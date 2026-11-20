"""Selection of the instances from the Zhang et al. (2024) dataset.

Phase 1 covers LM, LPL, LLF and MNC. Phase 2 (--phase 2) adds LTCE and CCC
from the same spreadsheet and writes a separate CSV, so the phase 1 list is
never touched. The rules below apply to both phases; the counts are those
of phase 1.

The universe is NOT everything Pysmell finds in the 311 files of the dataset
(that would give 333 snippets of the 4 smells). It is the subset the paper
itself kept: of the 687 detections, only 102 are Copilot-generated code, and
those are the ones in `results of RQ1.xlsx`. For the 4 smells, that is 89
occurrences in 83 distinct snippets. Using the 333 would mix human-written
code into a sample whose provenance is Copilot-generated code.

The instance is the FUNCTION that contains the smell, not the line. For LM
and LPL this makes no difference, because Pysmell measures the whole
function. For MNC it does: the metric is per expression, and a function full
of nested JSON triggers several lines (_process_data in GuardianRanks.py has
8). Counting by line would send the same code to the model several times and
count it as independent observations. Module-level code, outside any
function, is grouped as "<module>".

The enclosing function is the OUTERMOST one (module-level function or class
method), not the innermost. A nested function cannot be extracted alone
without changing its indentation, which would break the verbatim snippet,
and the function that contains it already carries it along: counting both
would send the same file twice. This only happens in the LPL of
first_pygame.py (heapify inside simulate_heapsort; partition and quicksort
inside simulate_quicksort). Grouped this way, the 83 snippets become 65
instances: MNC from 36 to 21, LPL from 22 to 19.

There is no sampling: every snippet goes in. The spreadsheet says WHICH
snippets; the ported Pysmell gives the METRICS of each one and works as a
check: if any snippet of the spreadsheet is not reproduced by the port, the
script fails instead of writing a partial list.

Usage:
    python -m data.selection.select             # phase 1, writes the default CSV
    python -m data.selection.select --phase 2   # phase 2 (LTCE, CCC)
    python -m data.selection.select --check     # only checks, does not write
"""

import argparse
import ast
import csv
import os
import sys
import warnings
from collections import Counter, defaultdict

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, ROOT)

from pysmell import validate_port  # noqa: E402
from pysmell._xlsx import read  # noqa: E402
from pysmell.detect import detect_file  # noqa: E402

SPREADSHEET = os.path.join(validate_port.ROOT, "results of RQ1.xlsx")
HERE = os.path.dirname(os.path.abspath(__file__))

# Per phase: the smells in id-numbering order (changing it renumbers every
# instance), their names in the spreadsheet and the default output CSV.
PHASES = {
    1: {
        "order": ("LM", "LPL", "LLF", "MNC"),
        "labels": validate_port.NAMES,
        "output": os.path.join(HERE, "instances_zhang.csv"),
    },
    2: {
        "order": ("LTCE", "CCC"),
        "labels": {
            "Long Ternary Conditional Expression": "LTCE",
            "Complex Container Comprehension": "CCC",
        },
        "output": os.path.join(HERE, "instances_zhang_phase2.csv"),
    },
}

# lines and metrics are lists when the function has more than one snippet:
#   lines   = "60;61;62"
#   metrics = "60:LEC=4|61:LEC=3|62:LEC=3"
FIELDS = ["id", "smell", "file", "function", "function_line", "lines",
          "metrics", "occurrences"]


def spreadsheet_snippets(all_files, labels):
    """Reads the RQ1 spreadsheet and returns {(path, line, smell): n_occurrences}.

    Groups by (file, line, smell) because the unit refactored is the snippet,
    and the paper itself (section 3.2.2) says the same snippet may show the
    same smell more than once. The concrete case is line 1473 of
    argos_ai_adventure.py, which appears twice for LLF.
    """
    occurrences = Counter()
    missing_file = []
    for row in read(SPREADSHEET)["Detected Code Smells"][1:]:
        if len(row) < 4 or row[3] not in labels:
            continue
        path = validate_port.locate(row[0], row[1], all_files)
        if path is None:
            missing_file.append(row[1])
            continue
        occurrences[(path, int(row[2]), labels[row[3]])] += 1
    if missing_file:
        raise SystemExit(
            "files in the spreadsheet that do not exist on disk: %s\n"
            "Download the dataset from Zenodo (see pysmell/README.md)." % missing_file
        )
    return occurrences


def file_metrics(paths, smells):
    """Runs the port only on the relevant files and indexes by (path, line, smell)."""
    measures = {}
    for path in sorted(paths):
        for item in detect_file(path, "tuning", smells=smells):
            measures[(path, item["line"], item["smell"])] = item["metrics"]
    return measures


def enclosing_function(path, line, _cache={}):
    """Returns (start_line, name) of the outermost function that contains the line.

    A nested function counts as part of the function that contains it (see
    the module docstring).

    The function is identified by its start line, not by its name: there are
    methods with the same name in different classes of the same file
    (my_image.py has two draw_line; cryptocurrency.py and network.py have two
    __init__ each). Outside any function it returns (0, "<module>").
    """
    if path not in _cache:
        with open(path, encoding="utf-8", errors="replace") as fh:
            source = fh.read()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            _cache[path] = ast.parse(source)
    best = None
    for node in ast.walk(_cache[path]):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.lineno <= line <= node.end_lineno:
                if best is None or node.lineno < best.lineno:
                    best = node
    return (best.lineno, best.name) if best else (0, "<module>")


def build(phase=1):
    """Returns the list of instances, with ids, or aborts if the port diverges."""
    order = PHASES[phase]["order"]
    all_files = list(validate_port.all_py())
    occurrences = spreadsheet_snippets(all_files, PHASES[phase]["labels"])
    measures = file_metrics({p for p, _, _ in occurrences}, order)

    missing = sorted(set(occurrences) - set(measures))
    if missing:
        for path, line, smell in missing:
            print("NOT REPRODUCED: %s:%d %s" % (path.split("/files/")[1], line, smell))
        raise SystemExit(
            "\n%d snippet(s) of the spreadsheet were not produced by the ported "
            "Pysmell. The list was not written: run pysmell/validate_port.py and "
            "resolve the divergence first." % len(missing)
        )

    # (smell, path, function_line) -> list of snippets of that function
    groups = defaultdict(list)
    names = {}
    for key in occurrences:
        path, line, smell = key
        start, name = enclosing_function(path, line)
        groups[(smell, path, start)].append(key)
        names[(path, start)] = name

    instances = []
    for smell in order:
        # Sorted by file and by the first detected line, so the id is always
        # the same, however many times the script runs.
        keys = sorted(
            (k for k in groups if k[0] == smell),
            key=lambda k: (k[1], min(line for _, line, _ in groups[k])),
        )
        for n, key in enumerate(keys, start=1):
            _, path, start = key
            snippets = sorted(groups[key])
            instances.append({
                "id": "%s-%02d" % (smell, n),
                "smell": smell,
                "file": path.split("/files/")[1],
                "function": names[(path, start)],
                "function_line": start,
                "lines": ";".join(str(line) for _, line, _ in snippets),
                "metrics": "|".join("%d:%s" % (s[1], measures[s]) for s in snippets),
                "occurrences": sum(occurrences[s] for s in snippets),
            })
    return instances


def main(argv=None):
    p = argparse.ArgumentParser(description="Selects the instances from Zhang et al.")
    p.add_argument("--phase", type=int, choices=sorted(PHASES), default=1)
    p.add_argument("--check", action="store_true",
                   help="only check and summarize, without writing the CSV")
    p.add_argument("--output", help="path of the output CSV (default depends on the phase)")
    args = p.parse_args(argv)
    order = PHASES[args.phase]["order"]
    output = args.output or PHASES[args.phase]["output"]

    instances = build(args.phase)
    n_snippets = Counter()
    for i in instances:
        n_snippets[i["smell"]] += len(i["lines"].split(";"))
    count = Counter(i["smell"] for i in instances)
    print("%-5s %8s %9s" % ("smell", "snippets", "instances"))
    for smell in order:
        print("%-5s %8d %9d" % (smell, n_snippets[smell], count[smell]))
    print("%-5s %8d %9d" % ("total", sum(n_snippets.values()), len(instances)))
    print("occurrences in the spreadsheet: %d" % sum(i["occurrences"] for i in instances))

    grouped = [i for i in instances if ";" in i["lines"]]
    print()
    print("instances with more than one snippet in the same function: %d" % len(grouped))
    for i in grouped:
        print("  %-6s %s  %s:%d  lines %s"
              % (i["id"], i["file"], i["function"], i["function_line"], i["lines"]))

    if args.check:
        return 0
    with open(output, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(instances)
    print("\nwritten: %s" % output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
