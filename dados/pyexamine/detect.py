"""Run the ported Pysmell (all 10 smells, Tuning Machine) on the PyExamine corpus.

Reads the .py files straight from the local zip built by extract_py.py and
writes one CSV row per detection (repository, file, line, smell, metrics)
plus a CSV of files that could not be analyzed (syntax error, too large,
recursion limit). Files are analyzed in parallel.

Usage:
    python -m dados.pyexamine.detect [--zip PATH] [--jobs N] [--limit N]
"""

import argparse
import ast
import csv
import os
import sys
import warnings
import zipfile
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from dados.pysmell import detectar
from dados.pysmell import astChecker

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dados" / "dataset_pyexamine"
DEFAULT_ZIP = DATA / "cloned_repositories_py.zip"
MAX_BYTES = 1_000_000  # larger files are almost always generated code
STRATEGY = detectar.ESTRATEGIAS["tuning"]

_zip = None


def _init(zip_path):
    global _zip
    _zip = zipfile.ZipFile(zip_path)
    sys.setrecursionlimit(10_000)


def analyze(name):
    """Return (name, detections, failure) for one file of the zip."""
    info = _zip.getinfo(name)
    if info.file_size > MAX_BYTES:
        return name, [], f"too large ({info.file_size} bytes)"
    source = _zip.read(name).decode("utf-8", errors="replace")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            tree = ast.parse(source)
        checker = astChecker.MyAst()
        checker.fileName = name
        checker.visit(tree)
    except SyntaxError as exc:
        return name, [], f"syntax error: {exc.msg}"
    except (RecursionError, ValueError, MemoryError) as exc:
        return name, [], f"{type(exc).__name__}"
    found = []
    for item in checker.result:
        rated = detectar._avaliar(item, STRATEGY)
        if rated is None:
            continue
        smell, metrics, detected = rated
        if detected:
            found.append((item[2], smell, ";".join(f"{k}={v}" for k, v in metrics.items())))
    return name, found, ""


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--zip", type=Path, default=DEFAULT_ZIP)
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--limit", type=int, default=0, help="analyze only the first N files")
    args = ap.parse_args(argv)

    with zipfile.ZipFile(args.zip) as z:
        names = sorted(n for n in z.namelist() if n.endswith(".py"))
    if args.limit:
        names = names[:args.limit]
    out = args.zip.parent / ("detections_sample.csv" if args.limit else "detections.csv")
    failures = out.with_name(out.stem + "_failures.csv")

    counts, failed = Counter(), 0
    with ProcessPoolExecutor(args.jobs, initializer=_init, initargs=(args.zip,)) as pool, \
            open(out, "w", newline="", encoding="utf-8") as fo, \
            open(failures, "w", newline="", encoding="utf-8") as ff:
        wo, wf = csv.writer(fo), csv.writer(ff)
        wo.writerow(["repo", "file", "line", "smell", "metrics"])
        wf.writerow(["repo", "file", "reason"])
        for i, (name, found, failure) in enumerate(pool.map(analyze, names, chunksize=64), 1):
            repo, _, path = name.partition("/")
            if failure:
                wf.writerow([repo, path, failure])
                failed += 1
            for line, smell, metrics in found:
                wo.writerow([repo, path, line, smell, metrics])
                counts[smell] += 1
            if i % 10_000 == 0:
                print(f"  {i:,}/{len(names):,} files", flush=True)

    print(f"files: {len(names):,}, not analyzed: {failed:,}")
    for smell, n in counts.most_common():
        print(f"  {smell:5} {n:,}")
    print(f"written: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
