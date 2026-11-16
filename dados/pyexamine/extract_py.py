"""Extract only the .py files from the PyExamine corpus on Zenodo.

The corpus is a single 22.5 GB zip (cloned_repositories.zip), and most of it
is .git folders. Zenodo serves HTTP Range requests, so this script reads the
zip's central directory from the end of the remote file, selects the .py
files outside .git, downloads only the byte ranges that hold them (nearby
files are merged into one request) and writes them to a local zip.

Each file is checked against the CRC-32 stored in the central directory.
The run can be resumed: files already in the output zip are skipped.

Usage:
    python -m dados.pyexamine.extract_py [--out PATH] [--dry-run]
"""

import argparse
import csv
import struct
import sys
import time
import urllib.request
import zipfile
import zlib
from pathlib import Path

RECORD = "14066039"
FILE_NAME = "cloned_repositories.zip"
URL = f"https://zenodo.org/api/records/{RECORD}/files/{FILE_NAME}/content"
PUBLISHED_MD5 = "6d42d1331aaacde1ca5930d621734470"
PREFIX = "cloned_repositories/"

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "dados" / "dataset_pyexamine" / "cloned_repositories_py.zip"

MAX_GAP = 64_000          # merge two files into one request if this close
MAX_SPAN = 32_000_000     # never request more than this at once
LOCAL_SLACK = 1_024       # room for the local header's own extra field


def fetch(start, end, retries=5):
    """Return bytes [start, end] of the remote zip (inclusive)."""
    req = urllib.request.Request(URL, headers={"Range": f"bytes={start}-{end}"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                if resp.status != 206:
                    raise RuntimeError(f"expected 206 Partial Content, got {resp.status}")
                data = resp.read()
            if len(data) != end - start + 1:
                raise RuntimeError(f"short read: {len(data)} of {end - start + 1} bytes")
            return data
        except Exception as exc:  # network errors are retried
            if attempt == retries - 1:
                raise
            wait = 2 ** attempt
            print(f"  retry in {wait}s after: {exc}", file=sys.stderr)
            time.sleep(wait)


def remote_size():
    req = urllib.request.Request(URL, method="HEAD")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return int(resp.headers["Content-Length"])


def central_directory(size):
    """Locate and download the central directory (zip64 aware)."""
    tail = fetch(size - 65_536, size - 1)
    eocd = tail.rfind(b"PK\x05\x06")
    if eocd < 0:
        raise RuntimeError("end of central directory not found")
    cd_size, cd_offset = struct.unpack("<II", tail[eocd + 12:eocd + 20])
    loc = tail.rfind(b"PK\x06\x07")
    if loc >= 0:
        (z64_offset,) = struct.unpack("<Q", tail[loc + 8:loc + 16])
        rec = fetch(z64_offset, z64_offset + 55)
        if rec[:4] != b"PK\x06\x06":
            raise RuntimeError("zip64 end of central directory not found")
        cd_size, cd_offset = struct.unpack("<QQ", rec[40:56])
    return fetch(cd_offset, cd_offset + cd_size - 1)


def parse_entries(cd):
    """Yield (name, method, crc, compressed, uncompressed, offset) per entry."""
    pos = 0
    while pos < len(cd):
        if cd[pos:pos + 4] != b"PK\x01\x02":
            raise RuntimeError(f"bad central directory entry at {pos}")
        method, = struct.unpack("<H", cd[pos + 10:pos + 12])
        crc, csize, usize = struct.unpack("<III", cd[pos + 16:pos + 28])
        nlen, xlen, clen = struct.unpack("<HHH", cd[pos + 28:pos + 34])
        offset, = struct.unpack("<I", cd[pos + 42:pos + 46])
        name = cd[pos + 46:pos + 46 + nlen].decode("utf-8", "replace")
        extra = cd[pos + 46 + nlen:pos + 46 + nlen + xlen]
        q = 0
        while q + 4 <= len(extra):
            hid, hsz = struct.unpack("<HH", extra[q:q + 4])
            body, r = extra[q + 4:q + 4 + hsz], 0
            if hid == 0x0001:  # zip64: only the fields that overflowed are present
                if usize == 0xFFFFFFFF:
                    usize, = struct.unpack("<Q", body[r:r + 8]); r += 8
                if csize == 0xFFFFFFFF:
                    csize, = struct.unpack("<Q", body[r:r + 8]); r += 8
                if offset == 0xFFFFFFFF:
                    offset, = struct.unpack("<Q", body[r:r + 8]); r += 8
            q += 4 + hsz
        yield name, method, crc, csize, usize, offset
        pos += 46 + nlen + xlen + clen


def wanted(name):
    return name.endswith(".py") and "/.git/" not in name and name.startswith(PREFIX)


def spans(entries):
    """Group entries (sorted by offset) into byte ranges to request."""
    group, start, end = [], None, None
    for e in entries:
        e_start = e[5]
        e_end = e_start + 30 + len(e[0].encode("utf-8")) + LOCAL_SLACK + e[3]
        if group and e_start - end <= MAX_GAP and e_end - start <= MAX_SPAN:
            group.append(e)
            end = max(end, e_end)
        else:
            if group:
                yield start, end, group
            group, start, end = [e], e_start, e_end
    if group:
        yield start, end, group


def read_member(blob, base, entry):
    """Decompress one member from a downloaded range and check its CRC."""
    name, method, crc, csize, _usize, offset = entry
    p = offset - base
    if blob[p:p + 4] != b"PK\x03\x04":
        raise RuntimeError(f"bad local header for {name}")
    nlen, xlen = struct.unpack("<HH", blob[p + 26:p + 30])
    start = p + 30 + nlen + xlen
    raw = blob[start:start + csize]
    if len(raw) != csize:
        raise RuntimeError(f"range too short for {name}")
    if method == 0:
        data = raw
    elif method == 8:
        data = zlib.decompressobj(-15).decompress(raw)
    else:
        raise RuntimeError(f"unsupported compression method {method} for {name}")
    if zlib.crc32(data) & 0xFFFFFFFF != crc:
        raise RuntimeError(f"CRC mismatch for {name}")
    return data


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help="output zip")
    ap.add_argument("--dry-run", action="store_true", help="only list what would be fetched")
    args = ap.parse_args(argv)

    size = remote_size()
    print(f"remote zip: {size:,} bytes (published md5 {PUBLISHED_MD5})")
    entries = sorted((e for e in parse_entries(central_directory(size)) if wanted(e[0])),
                     key=lambda e: e[5])
    print(f".py files outside .git: {len(entries):,}, "
          f"{sum(e[3] for e in entries) / 1e6:.1f} MB compressed")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if args.out.exists():
        with zipfile.ZipFile(args.out) as z:
            done = set(z.namelist())
    todo = [e for e in entries if e[0][len(PREFIX):] not in done]
    plan = list(spans(todo))
    print(f"already extracted: {len(done):,}; to fetch: {len(todo):,} files in "
          f"{len(plan):,} requests, {sum(b - a for a, b, _ in plan) / 1e6:.1f} MB")
    if args.dry_run or not plan:
        return 0

    manifest = args.out.with_suffix(".csv")
    new_manifest = not manifest.exists()
    with zipfile.ZipFile(args.out, "a", compression=zipfile.ZIP_DEFLATED) as z, \
            open(manifest, "a", newline="", encoding="utf-8") as mf:
        w = csv.writer(mf)
        if new_manifest:
            w.writerow(["path", "size", "crc32"])
        for i, (a, b, group) in enumerate(plan, 1):
            blob = fetch(a, b)
            for e in group:
                data = read_member(blob, a, e)
                path = e[0][len(PREFIX):]
                z.writestr(path, data)
                w.writerow([path, len(data), f"{e[2]:08x}"])
            if i % 50 == 0 or i == len(plan):
                print(f"  {i}/{len(plan)} requests", flush=True)
                mf.flush()
    print(f"done: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
