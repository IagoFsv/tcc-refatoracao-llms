"""
Descriptive analysis (step 7) of the two phases together.

Reads, for phases 1 and 2, the validation table (one row per generation), the
metrics table (originals and refactorings that preserved behavior) and the
extraction table, and writes summary tables. Nothing is measured here.

Rules:
  - preservation: share of generations that passed the 3 tests;
  - removal: share of removals among the generations that preserved, and
    share of generations that preserved AND removed over all generations;
  - metrics: percent change of each refactoring against the original unit of
    its instance, (refactored - original) / original * 100, aggregated in two
    levels: mean of the runs of each instance, then mean and sample standard
    deviation over the instances, so every instance weighs the same no matter
    how many of its runs preserved;
  - not applicable (left out of the means, never 0): MI when the Halstead
    volume is 0 on either side; any metric whose original value is 0 (the
    percent change is undefined; happens with the Pylint score); the Pysmell
    metrics of an expression, chain or container the refactoring removed
    (empty cell in metrics.csv);
  - Pysmell metrics are summarized only within their smell.

Groups: all, model, technique, model+technique, smell, smell+model,
smell+technique. Every table reports how many instances each group has.

Output, in results/analysis/:
    characterization.csv   instances, generations and extraction outcome per phase and smell
    preservation.csv       preservation rate per group
    removal.csv            removal rates per group
    metrics.csv            percent change per group and metric (mean, SD, n)
    instances.csv          per instance: preservations per model and technique
    ltce_ternary.csv       LTCE that preserved and removed: ternary left or not
    sessions.jsonl         commit of each run

Usage:
    python -m analysis.analyze
"""

import argparse
import csv
import datetime
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

from generation.generate import _commit
from validation.validate import PHASES, paths

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "analysis"

MODELS = ("qwen", "deepseek", "llama3")
TECHNIQUES = ("role", "few_shot", "chain_of_thought")
GENERAL = ("cc_max", "mi", "pylint")
SPECIFIC = {  # Pysmell metrics of each smell, as measured by metrics.measure
    "LLF": ("noc", "par", "noo"),
    "LTCE": ("noc", "nol"),
    "CCC": ("noc", "noff", "noo"),
    "MNC": ("lec", "dnc", "nct"),
}
GROUPS = {
    "all": lambda r: ("all",),
    "model": lambda r: (r["model"],),
    "technique": lambda r: (r["technique"],),
    "model+technique": lambda r: (r["model"], r["technique"]),
    "smell": lambda r: (r["smell"],),
    "smell+model": lambda r: (r["smell"], r["model"]),
    "smell+technique": lambda r: (r["smell"], r["technique"]),
}


# ------------------------------------------------------------------- reading

def _read(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def load():
    """(generations, originals, refactored), each row tagged with its phase."""
    generations, originals, refactored = [], {}, {}
    for phase in PHASES:
        extracted, validation_dir = paths(phase)
        status = {(r["model"], r["identifier"]): r["status"]
                  for r in _read(extracted / "extraction.csv")}
        for r in _read(validation_dir / "validation.csv"):
            r["phase"] = phase
            r["status"] = status[(r["model"], r["identifier"])]
            generations.append(r)
        for r in _read(ROOT / "results" / "metrics" / f"phase{phase}" / "metrics.csv"):
            if r["type"] == "original":
                originals[r["instance"]] = r
            else:
                refactored[(r["model"], r["identifier"])] = r
    return generations, originals, refactored


# ------------------------------------------------------------------- helpers

def _pct(part, whole):
    return round(100 * part / whole, 2) if whole else ""


def _value(key):
    return " | ".join(key)


def _float(x):
    return float(x) if x != "" else None


def change(metric, original, refactored):
    """Percent change of a metric, or None when not applicable."""
    if metric == "mi" and (float(original["volume"]) == 0 or float(refactored["volume"]) == 0):
        return None
    before, after = _float(original[metric]), _float(refactored[metric])
    if before is None or after is None or before == 0:
        return None
    return 100 * (after - before) / before


def _grouped(rows):
    """{(group, key): [rows]} for every group of GROUPS."""
    out = defaultdict(list)
    for name, keyf in GROUPS.items():
        for r in rows:
            out[(name, keyf(r))].append(r)
    return out


# -------------------------------------------------------------------- tables

def characterization(generations):
    rows = []
    for (phase, smell), gens in sorted(_by(generations, lambda r: (r["phase"], r["smell"])).items()):
        status = Counter(g["status"] for g in gens)
        reasons = Counter(g["reason"] for g in gens)
        rows.append({
            "phase": phase, "smell": smell,
            "instances": len({g["instance"] for g in gens}),
            "generations": len(gens),
            "block": status["block"], "open_fence": status["open fence"],
            "no_fence": status["no fence"], "no_code": status["no code"],
            "syntax_error": reasons["syntax"], "timeout": reasons["timeout"],
            "tests_failed": reasons["tests"],
            "preserved": sum(g["preserved"] == "1" for g in gens),
        })
    return rows


def preservation(generations):
    rows = []
    for (name, key), gens in _grouped(generations).items():
        preserved = sum(g["preserved"] == "1" for g in gens)
        rows.append({
            "group": name, "value": _value(key),
            "instances": len({g["instance"] for g in gens}),
            "generations": len(gens), "preserved": preserved,
            "preserved_pct": _pct(preserved, len(gens)),
        })
    return rows


def removal(generations):
    rows = []
    for (name, key), gens in _grouped(generations).items():
        kept = [g for g in gens if g["preserved"] == "1"]
        removed = sum(g["removed"] == "1" for g in kept)
        rows.append({
            "group": name, "value": _value(key),
            "instances": len({g["instance"] for g in gens}),
            "generations": len(gens), "preserved": len(kept), "removed": removed,
            "removed_pct_of_preserved": _pct(removed, len(kept)),
            "preserved_and_removed_pct_of_all": _pct(removed, len(gens)),
        })
    return rows


def metrics(generations, originals, refactored):
    pairs = []  # (generation row, metric, percent change)
    for g in generations:
        if g["preserved"] != "1":
            continue
        ref = refactored[(g["model"], g["identifier"])]
        orig = originals[g["instance"]]
        for m in GENERAL + SPECIFIC.get(g["smell"], ()):
            pc = change(m, orig, ref)
            if pc is not None:
                pairs.append((g, m, pc))

    rows = []
    for name, keyf in GROUPS.items():
        cells = defaultdict(lambda: defaultdict(list))  # (key, metric) -> instance -> [pc]
        for g, m, pc in pairs:
            if m not in GENERAL and "smell" not in name:
                continue
            cells[(keyf(g), m)][g["instance"]].append(pc)
        for (key, m), per_inst in cells.items():
            means = [statistics.mean(v) for v in per_inst.values()]
            rows.append({
                "group": name, "value": _value(key), "metric": m,
                "instances": len(means),
                "pairs": sum(len(v) for v in per_inst.values()),
                "mean_pct": round(statistics.mean(means), 2),
                "sd_pct": round(statistics.stdev(means), 2) if len(means) > 1 else "",
            })
    order = {m: i for i, m in enumerate(GENERAL + ("noc", "par", "noo", "nol", "noff", "lec", "dnc", "nct"))}
    rows.sort(key=lambda r: (list(GROUPS).index(r["group"]), r["value"], order[r["metric"]]))
    return rows


def instances(generations):
    rows = []
    for inst, gens in sorted(_by(generations, lambda r: r["instance"]).items()):
        row = {"instance": inst, "phase": gens[0]["phase"], "smell": gens[0]["smell"],
               "generations": len(gens)}
        for m in MODELS:
            row[f"preserved_{m}"] = sum(g["preserved"] == "1" for g in gens if g["model"] == m)
        for t in TECHNIQUES:
            row[f"preserved_{t}"] = sum(g["preserved"] == "1" for g in gens if g["technique"] == t)
        row["preserved"] = sum(g["preserved"] == "1" for g in gens)
        row["preserved_and_removed"] = sum(g["preserved"] == "1" and g["removed"] == "1" for g in gens)
        row["only_one_model"] = int(sum(row[f"preserved_{m}"] > 0 for m in MODELS) == 1)
        row["only_one_technique"] = int(sum(row[f"preserved_{t}"] > 0 for t in TECHNIQUES) == 1)
        rows.append(row)
    return rows


def ltce_ternary(generations, refactored):
    """LTCE that preserved and removed the smell: does a ternary remain in the file?

    With no ternary left (empty NOC) the expression became an if statement;
    with one left, it was shortened or reflowed below the thresholds.
    """
    done = [g for g in generations
            if g["smell"] == "LTCE" and g["preserved"] == "1" and g["removed"] == "1"]
    rows = []
    for name in ("all", "model", "technique"):
        for key, gens in sorted(_by(done, GROUPS[name]).items()):
            left = sum(refactored[(g["model"], g["identifier"])]["noc"] != "" for g in gens)
            rows.append({
                "group": name, "value": _value(key),
                "instances": len({g["instance"] for g in gens}),
                "preserved_and_removed": len(gens),
                "no_ternary_left": len(gens) - left, "ternary_left": left,
            })
    return rows


def _by(rows, keyf):
    out = defaultdict(list)
    for r in rows:
        out[keyf(r)].append(r)
    return out


# ---------------------------------------------------------------------- main

def _write(name, rows):
    path = OUTPUT / name
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"  {name}: {len(rows)} rows")


def main(argv=None):
    argparse.ArgumentParser(description="Descriptive analysis of the two phases.").parse_args(argv)
    generations, originals, refactored = load()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    print(f"{len(generations)} generations, {len(originals)} instances, "
          f"{len(refactored)} refactorings measured")
    _write("characterization.csv", characterization(generations))
    _write("preservation.csv", preservation(generations))
    _write("removal.csv", removal(generations))
    _write("metrics.csv", metrics(generations, originals, refactored))
    _write("instances.csv", instances(generations))
    _write("ltce_ternary.csv", ltce_ternary(generations, refactored))
    with open(OUTPUT / "sessions.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps({
            "start_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "commit": _commit(require_clean=False), "generations": len(generations)}) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
