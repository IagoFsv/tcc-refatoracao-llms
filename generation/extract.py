"""
Extraction of the refactored code from the raw responses (between steps 4 and 5).

The raw response (the generation JSON) is never changed: extraction reads the
JSON and writes the code to a separate file, so it can be redone at any time
with the same result. The rule follows the response formats seen in practice
(Llama 3 uses fences without a language; DeepSeek sometimes answers with code
only, without fences):

  1. Fenced blocks (```), with a python language (python, python3 or py,
     case-insensitive) or without a language: the LAST one counts. A block in
     another language (bash, text...) is ignored.
  2. A fence opened and never closed: the block goes from the opening to the
     end of the response.
  3. A response without any fence: the whole response counts, if ast.parse
     accepts it as Python.
  4. Otherwise: "no code", nothing is written and the generation counts as
     not preserving behavior.

The extracted code is not checked here (not even whether it compiles): that
is step 5.

Output, inside the phase folder:
    _extracted/<model>/<ID>__<technique>__s<seed>.py
    _extracted/extraction.csv   one row per generation, with its status

Usage:
    python -m generation.extract                                       # phase 1
    python -m generation.extract results/generations/_pilot/<session>
"""

import argparse
import ast
import csv
import json
import re
import sys
import warnings
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE1 = ROOT / "results" / "generations" / "phase1"

LANGUAGES = {"", "python", "python3", "py"}

# Fence at the start of the line, with an optional language. The closing one
# has nothing after the backticks.
OPEN = re.compile(r"^```\s*([^\s`]*)")
CLOSE = re.compile(r"^```\s*$")

COLUMNS = ["identifier", "model", "instance", "smell", "technique", "run",
           "seed", "done_reason", "status", "language", "blocks", "lines", "file"]


def blocks(text):
    """[(language, code, closed)] of the fenced blocks, in order."""
    found, current = [], None
    for line in text.splitlines():
        if current is None:
            m = OPEN.match(line)
            if m:
                current = (m.group(1).lower(), [])
        elif CLOSE.match(line):
            found.append((current[0], "\n".join(current[1]), True))
            current = None
        else:
            current[1].append(line)
    if current is not None:
        found.append((current[0], "\n".join(current[1]), False))
    return found


def _is_python(text):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            ast.parse(text)
        except (SyntaxError, ValueError):
            return False
    return True


def extract(text):
    """(code or None, status, language, number of blocks)."""
    every = blocks(text)
    if not every:
        if text.strip() and _is_python(text):
            return text.strip("\n"), "no fence", "", 0
        return None, "no code", "", 0
    candidates = [b for b in every if b[0] in LANGUAGES]
    if not candidates:
        return None, "no code", "", len(every)
    language, code, closed = candidates[-1]
    return code, "block" if closed else "open fence", language, len(every)


def main(argv=None):
    p = argparse.ArgumentParser(description="Extracts the code from the raw responses.")
    p.add_argument("folder", nargs="?", default=str(PHASE1),
                   help="phase folder (default: results/generations/phase1)")
    args = p.parse_args(argv)

    folder = Path(args.folder).resolve()
    records = sorted(f for f in folder.glob("*/*.json")
                     if not f.parent.name.startswith("_"))
    if not records:
        sys.exit(f"no generation in {folder}")
    output = folder / "_extracted"

    rows, counts = [], Counter()
    for f in records:
        d = json.loads(f.read_text(encoding="utf-8"))
        code, status, language, n = extract(d["response_text"])
        path = ""
        if code is not None:
            target = output / d["model"] / f"{f.stem}.py"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(code + "\n", encoding="utf-8", newline="\n")
            path = target.relative_to(folder).as_posix()
        rows.append({"identifier": f.stem, "model": d["model"],
                     "instance": d["instance"], "smell": d["smell"],
                     "technique": d["technique"], "run": d["run"],
                     "seed": d["seed"], "done_reason": d["done_reason"],
                     "status": status, "language": language, "blocks": n,
                     "lines": len(code.splitlines()) if code else 0,
                     "file": path})
        counts[d["model"], status] += 1

    output.mkdir(exist_ok=True)
    with open(output / "extraction.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)

    print(f"{len(records)} generations in {folder}")
    for model in sorted({m for m, _ in counts}):
        parts = ", ".join(f"{s} {c}" for (m, s), c in sorted(counts.items()) if m == model)
        print(f"  {model:9} {parts}")
    print(f"output in {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
