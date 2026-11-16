"""Python code smell detector (ported Pysmell), Tuning Machine strategy.

Thresholds and combination rules copied from pysmell/detection/detector.py in
the original repository (commit 233afeb). The original had no command line:
it was a script that read metric CSVs generated beforehand. Here both steps
(extracting metrics with astChecker and applying thresholds) live together.

Usage:
    python -m pysmell.detect <file_or_folder> [...] [options]

    --strategy {tuning,experience,statistics}  default: tuning
    --all         detects the 10 smells of Chen et al. (default: only STUDY_SMELLS)
    --metrics     also includes measurements below the threshold (to compare
                  original and refactored code in the metrics step)
    --output CSV  writes to a file instead of standard output

As a library:
    from pysmell.detect import detect_file, measure_file
"""

import argparse
import ast
import csv
import os
import sys
import warnings

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import astChecker  # noqa: E402

# Order of the thresholds in the original detector.py:
# [experience-based, statistics-based, tuning machine]
STRATEGIES = {"experience": 0, "statistics": 1, "tuning": 2}

PAR = [5, 4, 5]
MLOC = [38, 28, 52]
DOC = [3, 4, 4]
CLOC = [29, 59, 37]
LMC = [5, 4, 4]
NBC = [3, 2, 3]
NOC, LPAR, NOO = [48, 82, 73], [3, 3, 4], [7, 13, 15]
TNOC, TNOL = [54, 102, 101], [3, 3, 3]
CNOC, NOFF, CNOO = [62, 131, 92], [3, 3, 3], [8, 24, 22]
LEC, DNC, NCT = [3, 3, 3], [3, 4, 3], [3, 2, 2]

# Codes astChecker uses in result[0], with the smell abbreviation.
SMELLS = {
    1: ("LPL", "Long Parameter List"),
    2: ("LM", "Long Method"),
    3: ("LSC", "Long Scope Chaining"),
    4: ("LBCL", "Long Base Class List"),
    5: ("LC", "Large Class"),
    6: ("MNC", "Multiply-Nested Container"),
    9: ("LLF", "Long Lambda Function"),
    10: ("LTCE", "Long Ternary Conditional Expression"),
    11: ("CCC", "Complex Container Comprehension"),
    13: ("LMC", "Long Message Chain"),
}
STUDY_SMELLS = ("LM", "LPL", "LLF", "MNC")


def rate(item, k):
    """Returns (abbreviation, metrics, above_threshold) for an astChecker item."""
    code = item[0]
    if code not in SMELLS:
        return None
    abbr = SMELLS[code][0]
    if code == 1:
        return abbr, {"PAR": item[3]}, item[3] >= PAR[k]
    if code == 2:
        return abbr, {"MLOC": item[3]}, item[3] >= MLOC[k]
    if code == 3:
        return abbr, {"DOC": item[3]}, item[3] >= DOC[k]
    if code == 4:
        return abbr, {"NBC": item[3]}, item[3] >= NBC[k]
    if code == 5:
        return abbr, {"CLOC": item[3]}, item[3] >= CLOC[k]
    if code == 13:
        return abbr, {"LMC": item[3]}, item[3] >= LMC[k]
    if code == 9:
        m = {"NOC": item[3], "PAR": item[4], "NOO": item[5]}
        return abbr, m, item[3] >= NOC[k] and (item[4] >= LPAR[k] or item[5] >= NOO[k])
    if code == 10:
        m = {"NOC": item[3], "NOL": item[4]}
        return abbr, m, item[3] >= TNOC[k] or item[4] >= TNOL[k]
    if code == 11:
        m = {"NOC": item[3], "NOFF": item[4], "NOO": item[5]}
        return abbr, m, (item[3] >= CNOC[k] and item[5] >= CNOO[k]) or item[4] >= NOFF[k]
    if code == 6:
        # astChecker emits MNC in two forms: LEC (chain of indices) or
        # DNC+NCT (nesting of containers).
        if len(item) == 4:
            return abbr, {"LEC": item[3]}, item[3] >= LEC[k]
        m = {"DNC": item[3], "NCT": item[4]}
        return abbr, m, item[3] >= DNC[k] and item[4] >= NCT[k]
    return None


def measure_source(source, name="<source>"):
    """Runs astChecker on source code and returns every measurement, smell or not."""
    with warnings.catch_warnings():
        # Third-party code often has invalid escapes ("\d" outside a raw
        # string). That becomes a SyntaxWarning while parsing and is irrelevant here.
        warnings.simplefilter("ignore", SyntaxWarning)
        tree = ast.parse(source)
    checker = astChecker.MyAst()
    checker.fileName = name
    checker.visit(tree)
    return checker.result


def measure_file(path):
    """Runs astChecker on a file and returns every measurement, smell or not."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        return measure_source(fh.read(), path)


def detect_file(path, strategy="tuning", smells=STUDY_SMELLS, include_below=False):
    """Lists the smells of a file. Raises SyntaxError if the file does not parse."""
    k = STRATEGIES[strategy]
    found = []
    for item in measure_file(path):
        rated = rate(item, k)
        if rated is None:
            continue
        abbr, metrics, detected = rated
        if smells is not None and abbr not in smells:
            continue
        if not detected and not include_below:
            continue
        found.append({
            "file": path,
            "line": item[2],
            "smell": abbr,
            "detected": int(detected),
            "metrics": ";".join("%s=%s" % (n, v) for n, v in metrics.items()),
        })
    return found


def _files(targets):
    for target in targets:
        if os.path.isdir(target):
            for root, _, names in os.walk(target):
                for name in sorted(names):
                    if name.endswith(".py"):
                        yield os.path.join(root, name).replace(os.sep, "/")
        else:
            yield target.replace(os.sep, "/")


def main(argv=None):
    p = argparse.ArgumentParser(description="Ported Pysmell (Chen et al.), Python 3.")
    p.add_argument("targets", nargs="+", help=".py files or folders")
    p.add_argument("--strategy", choices=sorted(STRATEGIES), default="tuning")
    p.add_argument("--all", action="store_true", help="all 10 smells, not only STUDY_SMELLS")
    p.add_argument("--metrics", action="store_true", help="include measurements below the threshold")
    p.add_argument("--output", help="output CSV file")
    args = p.parse_args(argv)

    smells = None if args.all else STUDY_SMELLS
    rows, failures = [], []
    for path in _files(args.targets):
        try:
            rows.extend(detect_file(path, args.strategy, smells, args.metrics))
        except SyntaxError as error:
            failures.append((path, error))

    out = open(args.output, "w", newline="", encoding="utf-8") if args.output else sys.stdout
    writer = csv.DictWriter(out, fieldnames=["file", "line", "smell", "detected", "metrics"])
    writer.writeheader()
    writer.writerows(rows)
    if args.output:
        out.close()
        print("%d rows in %s" % (len(rows), args.output))

    for path, error in failures:
        print("does not parse (%s): %s" % (error.msg, path), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
