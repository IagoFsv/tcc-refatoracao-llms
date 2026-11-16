"""
Validation loop (step 5) over the extracted code of a phase.

Reads the `_extracted/extraction.csv` of the phase and, for each generation,
answers:
  preserved   the 3 tests of the instance pass on the extracted code;
  removed     Pysmell no longer detects the smell of the instance.

Rules:
  - "no code" in the extraction: not preserved, removed stays empty;
  - code that ast.parse rejects: not preserved, reason "syntax", removed
    stays empty (Pysmell does not measure what does not parse);
  - pytest running longer than TIMEOUT seconds: not preserved, reason
    "timeout";
  - removed is measured on all code that parses, preserving or not; the
    analysis filters by the ones that preserved.

The tests and units are the ones from step 3, unchanged. Resumable: a
generation already validated in the CSV does not run again. At the end, it
lists the suspicious instances (no generation preserved, or none removed the
smell).

Output, in results/validation/<phase>/:
    validation.csv   one row per generation
    suspicious.csv   flagged instances
    sessions.jsonl   commit, timeout and versions of each run

Usage:
    python -m validation.validate --sample 30   # tests, only prints
    python -m validation.validate               # whole phase
"""

import argparse
import ast
import csv
import datetime
import json
import sys
import time
import warnings
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from adaptation.checklist import _environment, _selection
from generation.generate import _commit
from validation.check import check

ROOT = Path(__file__).resolve().parents[1]
PHASE = "phase1"
EXTRACTED = ROOT / "results" / "generations" / PHASE / "_extracted"
OUTPUT = ROOT / "results" / "validation" / PHASE

TIMEOUT = 60  # seconds per generation (the 3 tests together)

COLUMNS = ["identifier", "model", "instance", "smell", "technique", "run",
           "seed", "extraction", "preserved", "reason", "tests", "removed",
           "remaining", "others", "seconds"]
SUSPICIOUS_COLUMNS = ["instance", "smell", "generations", "preserved", "removed", "reason"]


def _parses(path):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, ValueError):
            return False
    return True


def validate(row, inst):
    """Row of validation.csv for one row of extraction.csv."""
    base = {c: row[c] for c in ("identifier", "model", "instance", "smell",
                                "technique", "run", "seed")}
    base.update(extraction=row["status"], tests="", removed="",
                remaining="", others="", seconds=0)
    if not row["file"]:
        return {**base, "preserved": 0, "reason": "no code"}
    path = EXTRACTED.parent / row["file"]
    if not _parses(path):
        return {**base, "preserved": 0, "reason": "syntax"}
    start = time.perf_counter()
    res = check(inst, path, timeout=TIMEOUT)
    if res["preserved"]:
        reason = ""
    elif res["tests"] == "timeout":
        reason = "timeout"
    else:
        reason = "tests"
    return {**base, "preserved": int(res["preserved"]), "reason": reason,
            "tests": res["tests"], "removed": int(res["removed"]),
            "remaining": " | ".join(res["remaining"]), "others": " | ".join(res["others"]),
            "seconds": round(time.perf_counter() - start, 1)}


def _suspicious(rows):
    per_inst = defaultdict(list)
    for r in rows:
        per_inst[r["instance"]].append(r)
    flagged = []
    for ident, rs in sorted(per_inst.items()):
        preserved = sum(int(r["preserved"]) for r in rs)
        removed = sum(r["removed"] == "1" or r["removed"] == 1 for r in rs)
        reasons = [m for m, n in (("none preserved", preserved),
                                  ("none removed", removed)) if n == 0]
        if reasons:
            flagged.append({"instance": ident, "smell": rs[0]["smell"], "generations": len(rs),
                            "preserved": preserved, "removed": removed,
                            "reason": "; ".join(reasons)})
    return flagged


def main(argv=None):
    p = argparse.ArgumentParser(description="Validates the extracted code of a phase.")
    p.add_argument("--sample", type=int, metavar="N",
                   help="validate N generations spread over the phase and only print, writing nothing")
    p.add_argument("--jobs", type=int, default=4, help="pytest runs in parallel (default 4)")
    args = p.parse_args(argv)

    with open(EXTRACTED / "extraction.csv", encoding="utf-8", newline="") as fh:
        extraction = list(csv.DictReader(fh))
    selection = _selection()
    table = OUTPUT / "validation.csv"

    if args.sample:
        step = max(1, len(extraction) // args.sample)
        pending = extraction[::step][:args.sample]
        done = []
    else:
        commit = _commit(require_clean=True)
        OUTPUT.mkdir(parents=True, exist_ok=True)
        done = []
        if table.exists():
            with open(table, encoding="utf-8", newline="") as fh:
                done = list(csv.DictReader(fh))
        seen = {(r["model"], r["identifier"]) for r in done}
        pending = [r for r in extraction if (r["model"], r["identifier"]) not in seen]
        with open(OUTPUT / "sessions.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps({
                "start_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "commit": commit, "timeout_s": TIMEOUT, "jobs": args.jobs,
                "pending": len(pending), "environment": _environment()},
                ensure_ascii=False) + "\n")

    print(f"{len(extraction)} generations, {len(done)} already validated, {len(pending)} to validate")
    new = not table.exists()
    fh = None if args.sample else open(table, "a", encoding="utf-8", newline="")
    try:
        w = csv.DictWriter(fh, fieldnames=COLUMNS) if fh else None
        if w and new:
            w.writeheader()
        with ThreadPoolExecutor(max_workers=args.jobs) as ex:
            futures = [ex.submit(validate, r, selection[r["instance"]]) for r in pending]
            for i, f in enumerate(as_completed(futures), start=1):
                row = f.result()
                done.append(row)
                if w:
                    w.writerow(row)
                    fh.flush()
                if args.sample or i % 50 == 0 or i == len(pending):
                    print(f"  [{i}/{len(pending)}] {row['model']:9} {row['identifier']:32}"
                          f" preserved {row['preserved']} removed {'-' if row['removed'] == '' else row['removed']}"
                          f" {row['reason'] or ''} {row['tests']}")
    finally:
        if fh:
            fh.close()

    if not args.sample:
        # Re-sort the final CSV so it stays stable between runs.
        done.sort(key=lambda r: (r["model"], r["identifier"]))
        with open(table, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=COLUMNS)
            w.writeheader()
            w.writerows(done)

    total = len(done)
    preserved = sum(int(r["preserved"]) for r in done)
    print(f"\npreserved {preserved}/{total}")
    if len(done) == len(extraction):
        flagged = _suspicious(done)
        if not args.sample:
            with open(OUTPUT / "suspicious.csv", "w", encoding="utf-8", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=SUSPICIOUS_COLUMNS)
                w.writeheader()
                w.writerows(flagged)
        print(f"suspicious instances: {len(flagged)}")
        for s in flagged:
            print(f"  {s['instance']}: {s['reason']} ({s['preserved']} preserved,"
                  f" {s['removed']} removed, of {s['generations']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
