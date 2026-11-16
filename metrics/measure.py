"""
Quality metrics (step 6) of the original and of the refactorings that preserved behavior.

Measures, with the same tools, the original units of the phase and the
extracted code of every generation with preserved = 1 in validation.csv.

Measurement rules:
  - scope: the whole file (snippet + scaffolding), in every metric;
  - cc_max: the highest Radon CC among the functions of the file
    (module-level, methods and nested). Classes do not count: their CC is the
    sum of their methods;
  - LLF and MNC: Pysmell metrics of the largest case in the file; empty when
    there is nothing to measure ("not applicable", never 0).

Measured columns:
  cc_max        Radon, highest CC among the functions
  mi, mi_rank   Radon, maintainability index (0 to 100) and A/B/C rank, with
                the Radon default (a multi-line string counts as a comment)
  volume        Radon, Halstead volume of the file. Radon only counts
                arithmetic, unary, logical and comparison operators and `+=`;
                with none of them, the volume is 0 and MI is 100 by
                convention, without any computation. The analysis treats MI
                as not applicable when the volume is 0
  pylint        Pylint score (0 to 10), default configuration
  noc/par/noo   LLF only: the lambda with the highest NOC
  lec           MNC only: the longest chain of indices
  dnc/nct       MNC only: the container with the highest DNC (tie: highest NCT)

Pylint runs in a temporary folder, with the file copied under the name of
the original unit (LM_01.py etc.), so the module name is the same in the
original and in the refactored code, and with an empty configuration file,
so no configuration of the machine gets in.

Percent changes and means are computed in step 7 (analysis/).

Output, in results/metrics/<phase>/:
    metrics.csv      one row per measured file (originals and refactored)
    sessions.jsonl   commit and tool versions of each run

Usage:
    python -m metrics.measure --sample 10   # tests, only prints
    python -m metrics.measure               # whole phase
"""

import argparse
import csv
import datetime
import importlib.metadata
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from radon.complexity import cc_visit
from radon.metrics import h_visit, mi_rank, mi_visit

from adaptation.checklist import _paths, _selection
from generation.generate import _commit
from pysmell.detect import detect_file
from validation.validate import EXTRACTED, PHASE, OUTPUT as VALIDATION

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "metrics" / PHASE

PACKAGES = ("radon", "pylint", "astroid", "astunparse")
PYLINT_TIMEOUT = 120  # seconds per file

COLUMNS = ["type", "identifier", "model", "instance", "smell", "technique",
           "run", "seed", "cc_max", "mi", "mi_rank", "volume", "pylint",
           "noc", "par", "noo", "lec", "dnc", "nct"]


def _environment():
    versions = [f"Python {platform.python_version()}"]
    for package in PACKAGES:
        versions.append(f"{package} {importlib.metadata.version(package)}")
    return "; ".join(versions)


# ---------------------------------------------------------------- Radon

def _functions(blocks):
    """Functions, methods and nested functions (Radon keeps the latter in closures)."""
    for b in blocks:
        if hasattr(b, "methods"):  # class
            yield from _functions(b.methods)
        else:
            yield b
            yield from _functions(b.closures)


def _radon(code):
    complexities = [f.complexity for f in _functions(cc_visit(code))]
    mi = mi_visit(code, multi=True)
    return {"cc_max": max(complexities) if complexities else "",
            "mi": round(mi, 2), "mi_rank": mi_rank(mi),
            "volume": round(h_visit(code).total.volume, 2)}


# ---------------------------------------------------------------- Pylint

def _pylint(path, name):
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        shutil.copy(path, Path(tmp, name))
        rc = Path(tmp, "empty.rc")
        rc.write_text("", encoding="utf-8")
        env = {k: v for k, v in os.environ.items() if k != "PYLINTRC"}
        r = subprocess.run(
            [sys.executable, "-m", "pylint", f"--rcfile={rc}", "--persistent=n",
             "--output-format=json2", name],
            cwd=tmp, capture_output=True, text=True, timeout=PYLINT_TIMEOUT, env=env)
    try:
        return round(json.loads(r.stdout)["statistics"]["score"], 2)
    except (ValueError, KeyError) as error:
        raise RuntimeError(f"Pylint gave no score for {path}: {r.stderr[-500:]}") from error


# ---------------------------------------------------------------- Pysmell

def _values(detection):
    return {k.lower(): int(v) for k, v in
            (pair.split("=") for pair in detection["metrics"].split(";"))}


def _pysmell(path, smell):
    empty = {c: "" for c in ("noc", "par", "noo", "lec", "dnc", "nct")}
    if smell not in ("LLF", "MNC"):
        return empty
    measures = [_values(d) for d in
                detect_file(str(path), smells=(smell,), include_below=True)]
    if smell == "LLF":
        if measures:
            largest = max(measures, key=lambda m: m["noc"])
            empty.update(noc=largest["noc"], par=largest["par"], noo=largest["noo"])
        return empty
    lecs = [m["lec"] for m in measures if "lec" in m]
    containers = [m for m in measures if "dnc" in m]
    if lecs:
        empty["lec"] = max(lecs)
    if containers:
        largest = max(containers, key=lambda m: (m["dnc"], m["nct"]))
        empty.update(dnc=largest["dnc"], nct=largest["nct"])
    return empty


# ---------------------------------------------------------------- measurement

def measure(base, path, inst):
    code = Path(path).read_text(encoding="utf-8")
    _, unit, _, _ = _paths(inst)
    return {**base, **_radon(code), "pylint": _pylint(path, unit.name),
            **_pysmell(path, inst["smell"])}


def _tasks(selection):
    """(base, path, inst) of the originals and of the refactorings that preserved."""
    with open(VALIDATION / "validation.csv", encoding="utf-8", newline="") as fh:
        validation = list(csv.DictReader(fh))
    ids = sorted({r["instance"] for r in validation})
    tasks = []
    for ident in ids:
        inst = selection[ident]
        base = {c: "" for c in COLUMNS}
        base.update(type="original", identifier=ident, instance=ident, smell=inst["smell"])
        tasks.append((base, _paths(inst)[1], inst))
    for r in validation:
        if r["preserved"] != "1":
            continue
        base = {c: "" for c in COLUMNS}
        base.update({c: r[c] for c in ("identifier", "model", "instance", "smell",
                                       "technique", "run", "seed")}, type="refactored")
        tasks.append((base, EXTRACTED / r["model"] / f"{r['identifier']}.py",
                      selection[r["instance"]]))
    return tasks


def main(argv=None):
    p = argparse.ArgumentParser(description="Metrics of the original and of the refactorings that preserved.")
    p.add_argument("--sample", type=int, metavar="N",
                   help="measure N files spread over the phase and only print, writing nothing")
    p.add_argument("--jobs", type=int, default=4, help="files in parallel (default 4)")
    args = p.parse_args(argv)

    tasks = _tasks(_selection())
    table = OUTPUT / "metrics.csv"
    if args.sample:
        tasks = tasks[::max(1, len(tasks) // args.sample)][:args.sample]
    else:
        if table.exists():
            sys.exit(f"{table} already exists. Measured results are not overwritten; "
                     "delete it by hand if you really mean to measure again.")
        commit = _commit(require_clean=True)
        OUTPUT.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT / "sessions.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps({
                "start_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "commit": commit, "files": len(tasks), "environment": _environment()},
                ensure_ascii=False) + "\n")

    print(f"{len(tasks)} files to measure")
    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        rows = list(ex.map(lambda t: measure(*t), tasks))

    if args.sample:
        for r in rows:
            print(f"  {r['type']:10} {r['model'] or '-':8} {r['identifier']:32} "
                  f"cc_max {r['cc_max']} mi {r['mi']} ({r['mi_rank']}) vol {r['volume']} pylint {r['pylint']} "
                  + " ".join(f"{c}={r[c]}" for c in ("noc", "par", "noo", "lec", "dnc", "nct")
                             if r[c] != ""))
        return 0

    rows.sort(key=lambda r: (r["type"] != "original", r["model"], r["identifier"]))
    with open(table, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    n_orig = sum(r["type"] == "original" for r in rows)
    print(f"{n_orig} originals and {len(rows) - n_orig} refactored in {table}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
