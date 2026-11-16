"""Checks the Pysmell port against the Zhang et al. (2024) dataset.

The paper (section 3.1) says Pysmell was run on the 311 files with the
Tuning Machine strategy, producing 687 detections, of which 102 were kept
because they are Copilot-generated code (57 in Repositories, 45 in Code).
The 102 are in `results of RQ1.xlsx`.

This script runs the port on the same files and compares. It is evidence
that the port reproduces the original detector, and must be run again if
astChecker.py, compat.py or detect.py change.

Usage:
    python -m pysmell.validate_port
"""

import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _xlsx import read  # noqa: E402
from detect import STUDY_SMELLS, detect_file  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "dataset_zhang", "dataset")
ROOT = os.path.normpath(ROOT).replace(os.sep, "/")
FILES = ROOT + "/files"

# Names as they appear in the spreadsheet -> abbreviations used in the port.
NAMES = {
    "Long Method": "LM",
    "Long Parameter List": "LPL",
    "Long Lambda Function": "LLF",
    "Multiply Nested Container": "MNC",
}

# What the paper reports, for comparison.
PAPER = {"total": 687, "Repositories": 57, "Code": 630}


def all_py():
    """Public because data/selection/select.py reuses it (a single implementation)."""
    for root, _, names in os.walk(FILES):
        for name in sorted(names):
            if name.endswith(".py"):
                yield os.path.join(root, name).replace(os.sep, "/")


def locate(source, spreadsheet_path, all_files):
    """Public because data/selection/select.py reuses it.

    The spreadsheet uses 'code/x.py' and 'repo/a/b.py'; on disk they are Code/ and Repositories/."""
    prefix = "/Code/" if source == "code" else "/Repositories/"
    base = os.path.basename(spreadsheet_path)
    candidates = [p for p in all_files if prefix in p and os.path.basename(p) == base]
    if len(candidates) > 1:
        tail = spreadsheet_path.split("/", 1)[1]
        candidates = [p for p in candidates if p.endswith(tail)] or candidates
    return candidates[0] if candidates else None


def main():
    files = list(all_py())
    print(".py files found: %d (paper: 311)" % len(files))

    expected, occurrences, missing_file = set(), Counter(), []
    rows = read(ROOT + "/results of RQ1.xlsx")["Detected Code Smells"][1:]
    for row in rows:
        if len(row) < 4 or row[3] not in NAMES:
            continue
        path = locate(row[0], row[1], files)
        if path is None:
            missing_file.append(row[1])
            continue
        abbr = NAMES[row[3]]
        occurrences[abbr] += 1
        expected.add((path, int(row[2]), abbr))
    print("RQ1 spreadsheet: %d occurrences of the 4 smells, %d distinct snippets"
          % (sum(occurrences.values()), len(expected)))
    print("  occurrences:", dict(occurrences))
    print("  distinct snippets:", dict(Counter(s for _, _, s in expected)))
    if missing_file:
        print("  FILE NOT ON DISK:", missing_file)

    detected, per_folder, failures = set(), Counter(), []
    for path in files:
        try:
            found = detect_file(path, "tuning", smells=None)
        except SyntaxError as error:
            failures.append((path, error.msg))
            continue
        for item in found:
            per_folder["Repositories" if "/Repositories/" in path else "Code"] += 1
            if item["smell"] in STUDY_SMELLS:
                detected.add((path, item["line"], item["smell"]))

    print("\nport, tuning strategy, 10 smells:")
    print("  total: %d (paper: %d)" % (sum(per_folder.values()), PAPER["total"]))
    for folder in ("Repositories", "Code"):
        print("  %s: %d (paper: %d)" % (folder, per_folder[folder], PAPER[folder]))
    if failures:
        print("  do not parse: %d" % len(failures))
        for path, msg in failures:
            print("    %s (%s)" % (path.split("/files/")[1], msg))

    missing = expected - detected
    print("\nreproduction of the Zhang et al. snippets: %d/%d" % (len(expected & detected), len(expected)))
    for path, line, abbr in sorted(missing):
        print("  NOT REPRODUCED: %s:%d %s" % (path.split("/files/")[1], line, abbr))
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
