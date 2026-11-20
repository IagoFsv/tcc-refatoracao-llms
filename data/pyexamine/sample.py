"""Sampling of the phase 2 instances from the PyExamine corpus (LTCE and CCC).

Input: the detections of the ported Pysmell over the corpus (detections.csv,
written by data/pyexamine/detect.py) and the zip with the .py files.

The instance is the FUNCTION that contains the smell, with the same rules as
data/selection/select.py: the outermost function (module-level function or
class method); several detections in the same function are one instance;
code outside any function is grouped as "<module>", one per file and smell.

Before the draw, every unit goes through these rules, in this order, and the
first one that fails is the reason it is left out:

1. duplicate repository: a repository whose .py files are all identical
   (same CRC-32 and size) to those of a repository with a smaller name
   (e.g. a mirror of the same project under another name);
2. test file: inside a folder named tests, test or testing, or named
   test_*.py, *_test.py or conftest.py;
3. external name: the unit, plus everything of the same file it depends on
   (followed transitively), uses a name that is not a builtin, does not come
   from the standard library and is not defined in the file itself. For a
   method, the bases and __init__ of its class are checked too, since the
   class has to be instantiated. Relative imports and imports of the
   project's own package count as external;
4. too large: the unit plus the top-level code of the file it depends on
   exceeds MAX_CHARS, so the prompt would not fit in the context window.

The units that pass are the eligible ones. For each smell, they are sorted in
a fixed order (repository, file, function line) and shuffled with
random.Random(SEED). The whole shuffled list is written, with its rank. The
instances are the first CAP of the list; if an instance is later excluded
during adaptation (instances/excluded.csv), the next one in the list takes
its place, so the replacement never depends on a choice.

The ids continue the numbering of the Zhang instances of the same smell
(data/selection/instances_zhang_phase2.csv), in rank order. An excluded
instance keeps its id.

This script only parses the corpus code (ast); it never runs it.

Usage:
    python -m data.pyexamine.sample            # writes the CSVs
    python -m data.pyexamine.sample --check    # only summarizes
"""

import argparse
import ast
import builtins
import csv
import random
import sys
import warnings
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "dataset_pyexamine"
SELECTION = ROOT / "data" / "selection"
ZIP = DATA / "cloned_repositories_py.zip"
DETECTIONS = DATA / "detections.csv"
INDEX = DATA / "cloned_repositories_py.csv"
ZHANG = SELECTION / "instances_zhang_phase2.csv"
EXCLUDED = ROOT / "instances" / "excluded.csv"
CANDIDATES = SELECTION / "candidates_pyexamine.csv"
INSTANCES = SELECTION / "instances_pyexamine.csv"
SUMMARY = SELECTION / "filter_pyexamine.csv"

SMELLS = ("LTCE", "CCC")
SEED = 42
CAP = 10
# About the size of the largest unit whose prompt fit in the context window
# of every model (7,189 characters).
MAX_CHARS = 7000

TEST_DIRS = {"tests", "test", "testing"}
STDLIB = set(sys.stdlib_module_names) | {"__future__"}
BUILTIN_NAMES = set(dir(builtins)) | {
    "__file__", "__name__", "__doc__", "__spec__", "__package__", "__loader__",
    "__builtins__", "__path__",
}

REASONS = ("duplicate repository", "test file", "external name", "too large", "eligible")
CANDIDATE_FIELDS = ["rank", "smell", "repo", "file", "function", "function_line",
                    "lines", "metrics", "chars"]
INSTANCE_FIELDS = ["id"] + CANDIDATE_FIELDS


def duplicate_repositories(index_path):
    """Repositories whose set of .py files equals that of a smaller-named one."""
    files = defaultdict(set)
    with open(index_path, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            repo = row["path"].split("/", 1)[0]
            files[repo].add((row["path"].split("/", 1)[1], row["crc32"], row["size"]))
    seen, duplicates = {}, {}
    for repo in sorted(files):
        content = frozenset((crc, size) for _, crc, size in files[repo])
        if content in seen:
            duplicates[repo] = seen[content]
        else:
            seen[content] = repo
    return duplicates


def is_test_file(path):
    parts = path.split("/")
    name = parts[-1]
    return (any(p in TEST_DIRS for p in parts[:-1])
            or name.startswith("test_") or name.endswith("_test.py")
            or name == "conftest.py")


def _import_kind(node):
    """'std' or 'external' for an Import/ImportFrom node."""
    if isinstance(node, ast.ImportFrom):
        top = (node.module or "").split(".")[0]
        return "std" if node.level == 0 and top in STDLIB else "external"
    return None


def module_bindings(tree):
    """Maps each top-level name to ('import', 'std'|'external') or ('local', node).

    'local' points to the top-level statement that defines the name. Imports
    and definitions inside top-level if/try blocks (conditional imports,
    fallbacks) count too.
    """
    env = {}

    def bind(name, kind):
        # A name imported both ways (try: import ujson as json / except
        # ImportError: import json) runs with the standard library alone.
        current = env.get(name)
        if current is None or (kind == "std" and current[0] == "import"):
            env[name] = ("import", kind)

    def bind_import(node):
        if isinstance(node, ast.Import):
            for alias in node.names:
                top = alias.name.split(".")[0]
                bind(alias.asname or top, "std" if top in STDLIB else "external")
        else:
            kind = _import_kind(node)
            for alias in node.names:
                if alias.name != "*":
                    bind(alias.asname or alias.name, kind)
                elif env.get("*") != ("import", "external"):
                    # Any name not bound in the file is assumed to come from
                    # the star import; one external star import is enough to
                    # make every such name external.
                    env["*"] = ("import", kind)

    def bind_targets(targets, owner):
        for target in targets:
            for n in ast.walk(target):
                if isinstance(n, ast.Name):
                    env.setdefault(n.id, ("local", owner))

    for stmt in tree.body:
        for node in ast.walk(stmt) if isinstance(stmt, (ast.If, ast.Try)) else [stmt]:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                bind_import(node)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if node is stmt or isinstance(stmt, (ast.If, ast.Try)):
                    env.setdefault(node.name, ("local", stmt))
            elif isinstance(node, ast.Assign):
                bind_targets(node.targets, stmt)
            elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
                bind_targets([node.target], stmt)
    return env


def free_names(node):
    """Names read inside the node that are not bound inside it."""
    bound, used = set(), set()
    for n in ast.walk(node):
        if isinstance(n, ast.Name):
            (bound if isinstance(n.ctx, (ast.Store, ast.Del)) else used).add(n.id)
        elif isinstance(n, ast.arg):
            bound.add(n.arg)
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n is not node:
            bound.add(n.name)
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            for alias in n.names:
                bound.add((alias.asname or alias.name).split(".")[0])
        elif isinstance(n, ast.ExceptHandler) and n.name:
            bound.add(n.name)
    return used - bound


def dependencies(start, env):
    """Top-level statements the start nodes need, or (None, name) if a name is external."""
    seen, stack = {}, list(start)
    while stack:
        node = stack.pop()
        if id(node) in seen:
            continue
        seen[id(node)] = node
        for name in sorted(free_names(node)):
            if name in BUILTIN_NAMES:
                continue
            binding = env.get(name) or env.get("*")
            if binding is None:
                return None, name
            if binding[0] == "import":
                if binding[1] == "external":
                    return None, name
                continue
            stack.append(binding[1])
    return list(seen.values()), None


def text_length(lines, node):
    first = min([node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])])
    return sum(len(line) + 1 for line in lines[first - 1:node.end_lineno])


def outermost_function(tree, line):
    """(function node, enclosing class node or None) of the outermost function with the line."""
    best = None
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.lineno <= line <= node.end_lineno and (best is None or node.lineno < best.lineno):
                best = node
    if best is None:
        return None, None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and best in node.body:
            return best, node
    return best, None


def evaluate_unit(tree, lines, env, function, cls, detection_lines):
    """Returns (reason, chars) for one unit; reason is 'eligible' if it passes."""
    if function is None:
        start = [s for s in tree.body
                 if any(s.lineno <= n <= s.end_lineno for n in detection_lines)]
    else:
        start = [function]
        if cls is not None:
            start += list(cls.bases) + list(cls.keywords) + list(cls.decorator_list)
            start += [m for m in cls.body
                      if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)) and m.name == "__init__"]
    nodes, _ = dependencies(start, env)
    if nodes is None:
        return "external name", 0
    top = {id(s) for s in tree.body}
    chars = sum(text_length(lines, n) for n in nodes
                if id(n) in top or n is function or (cls is not None and n in cls.body))
    if chars > MAX_CHARS:
        return "too large", chars
    return "eligible", chars


def read_detections(path):
    """{(repo, file): {smell: [(line, metrics)]}} for the sampled smells."""
    out = defaultdict(lambda: defaultdict(list))
    with open(path, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["smell"] in SMELLS:
                out[(row["repo"], row["file"])][row["smell"]].append((int(row["line"]), row["metrics"]))
    return out


def build(zip_path=ZIP, detections_path=DETECTIONS, index_path=INDEX):
    """Returns (eligible units by smell, Counter of reasons by smell)."""
    duplicates = duplicate_repositories(index_path)
    detections = read_detections(detections_path)
    reasons = {s: Counter() for s in SMELLS}
    eligible = {s: [] for s in SMELLS}
    with zipfile.ZipFile(zip_path) as z:
        for (repo, file), by_smell in sorted(detections.items()):
            file_reason = ("duplicate repository" if repo in duplicates
                           else "test file" if is_test_file(file) else None)
            source = z.read(f"{repo}/{file}").decode("utf-8", errors="replace")
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                tree = ast.parse(source)
            lines = source.splitlines()
            env = module_bindings(tree)
            for smell, found in sorted(by_smell.items()):
                units, owners = defaultdict(list), {}
                for line, metrics in found:
                    function, cls = outermost_function(tree, line)
                    key = (function.lineno, function.name) if function else (0, "<module>")
                    units[key].append((line, metrics))
                    owners[key] = (function, cls)
                for key, items in sorted(units.items()):
                    if file_reason is not None:
                        reasons[smell][file_reason] += 1
                        continue
                    function, cls = owners[key]
                    items = sorted(set(items))
                    reason, chars = evaluate_unit(tree, lines, env, function, cls,
                                                  [line for line, _ in items])
                    reasons[smell][reason] += 1
                    if reason == "eligible":
                        eligible[smell].append({
                            "smell": smell, "repo": repo, "file": file,
                            "function": key[1], "function_line": key[0],
                            "lines": ";".join(str(line) for line, _ in items),
                            "metrics": "|".join(f"{line}:{m}" for line, m in items),
                            "chars": chars,
                        })
    return eligible, reasons, duplicates


def shuffled(units):
    """Fixed order, then shuffled with the seed; adds the rank."""
    ordered = sorted(units, key=lambda u: (u["repo"], u["file"], u["function_line"]))
    random.Random(SEED).shuffle(ordered)
    return [dict(u, rank=i) for i, u in enumerate(ordered, start=1)]


def zhang_counts(path=ZHANG):
    with open(path, encoding="utf-8") as fh:
        return Counter(row["smell"] for row in csv.DictReader(fh))


def excluded_ids(path=EXCLUDED):
    if not path.exists():
        return set()
    with open(path, encoding="utf-8") as fh:
        return {row["id"] for row in csv.DictReader(fh)}


def pick(ranked, smell, offset, excluded):
    """First CAP non-excluded units in rank order; excluded ones keep their id."""
    chosen, kept = [], 0
    for n, unit in enumerate(ranked, start=offset + 1):
        uid = f"{smell}-{n:02d}"
        chosen.append(dict(unit, id=uid))
        if uid not in excluded:
            kept += 1
        if kept == CAP:
            break
    return chosen


def write_csv(path, fields, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows({k: r[k] for k in fields} for r in rows)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--check", action="store_true", help="only summarize, without writing")
    args = p.parse_args(argv)

    eligible, reasons, duplicates = build()
    offsets = zhang_counts()
    excluded = excluded_ids()

    print("duplicate repositories: " + ", ".join(f"{d} (= {o})" for d, o in sorted(duplicates.items())))
    print("%-22s %8s %8s" % ("units", *SMELLS))
    for reason in REASONS:
        print("%-22s %8d %8d" % (reason, *(reasons[s][reason] for s in SMELLS)))

    candidates, instances = [], []
    for smell in SMELLS:
        ranked = shuffled(eligible[smell])
        candidates += ranked
        chosen = pick(ranked, smell, offsets[smell], excluded)
        instances += chosen
        repos = len({u["repo"] for u in eligible[smell]})
        print(f"{smell}: {len(ranked)} eligible in {repos} repositories; "
              f"ids {chosen[0]['id']} to {chosen[-1]['id']}")

    if args.check:
        return 0
    write_csv(CANDIDATES, CANDIDATE_FIELDS, candidates)
    write_csv(INSTANCES, INSTANCE_FIELDS, instances)
    write_csv(SUMMARY, ["smell", "reason", "units"],
              [{"smell": s, "reason": r, "units": reasons[s][r]} for s in SMELLS for r in REASONS])
    for path in (CANDIDATES, INSTANCES, SUMMARY):
        print(f"written: {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
