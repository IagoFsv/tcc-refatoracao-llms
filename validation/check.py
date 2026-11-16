"""Validation of one LLM-generated refactoring (step 5).

For an instance and a refactored file, checks:
  preservation   the 3 tests of the instance pass on the file;
  removal        Pysmell no longer detects the smell of the instance in the file.

The two answers are independent: the analysis measures removal only in the
refactorings that preserve behavior.

Usage:
    python -m validation.check LLF-01 path.py
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from adaptation.checklist import _paths, _pytest, _selection
from pysmell.detect import detect_file


def check(inst, path, timeout=None):
    """{tests, preserved, remaining, others, removed} of a refactored file.

    With a timeout (seconds), a pytest run that exceeds it counts as not
    preserved and `tests` becomes "timeout".
    """
    _, unit, test, _ = _paths(inst)
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        shutil.copy(path, Path(tmp, unit.name))
        shutil.copy(test, tmp)
        try:
            r = _pytest(Path(tmp), timeout=timeout)
        except subprocess.TimeoutExpired:
            r = None
    if r is None:
        last = "timeout"
    else:
        last = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
    detections = detect_file(str(path))
    remaining = [f"{d['smell']} L{d['line']} {d['metrics']}"
                 for d in detections if d["smell"] == inst["smell"]]
    others = [f"{d['smell']} L{d['line']} {d['metrics']}"
              for d in detections if d["smell"] != inst["smell"]]
    return {
        "tests": last,
        "preserved": r is not None and r.returncode == 0 and "3 passed" in last,
        "remaining": remaining,
        "others": others,
        "removed": not remaining,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Validates one refactoring of an instance.")
    p.add_argument("id", help="instance id (e.g. LLF-01)")
    p.add_argument("file", help="refactored file")
    args = p.parse_args(argv)

    selection = _selection()
    if args.id not in selection:
        p.error(f"id not in the selection: {args.id}")
    inst = selection[args.id]
    res = check(inst, args.file)
    print(f"{inst['id']}: {args.file}")
    print(f"  pytest: {res['tests']}")
    print(f"  remaining {inst['smell']}: {', '.join(res['remaining']) or 'none'}")
    if res["others"]:
        print(f"  other smells: {', '.join(res['others'])}")
    print(f"  preserved: {'yes' if res['preserved'] else 'no'}"
          f" | removed: {'yes' if res['removed'] else 'no'}")
    return 0 if res["preserved"] else 1


if __name__ == "__main__":
    sys.exit(main())
