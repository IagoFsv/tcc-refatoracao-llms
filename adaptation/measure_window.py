"""Measures the prompt of each instance in each model, for the context window criterion.

Criterion: the prompt must fit in num_ctx - num_predict tokens in EVERY
model, otherwise prompt + output exceed the window. An instance that does
not fit is removed for every model, before generation.

Method: the prompt built by generation/prompts.py goes to the Ollama
/api/chat with num_predict 1 and keep_alive 0, and the count is the
prompt_eval_count of the response (model template included). keep_alive 0
unloads the model at every call, so the prefix cache does not reduce the
count. By default only Few-Shot is measured: with the same core plus one
example, it is always the largest of the three prompts.

Usage:
    python -m adaptation.measure_window                 # every instance
    python -m adaptation.measure_window LM-04 MNC-01    # only these
    --technique role|few_shot|chain_of_thought

Writes instances/window.csv, one row per instance, with the count in each
model. Rows of instances that were not measured now are kept.
"""

import argparse
import csv
import datetime
import sys
from pathlib import Path

import yaml

from generation import client, prompts

ROOT = Path(__file__).resolve().parent.parent
INSTANCES = ROOT / "instances"
TABLE = INSTANCES / "window.csv"


def _units(ids):
    """{id: unit path} of the instances that have a folder (or only the requested ones)."""
    everything = {p.parent.name: p for p in sorted(INSTANCES.glob("*/*/*.py"))
                  if p.stem == p.parent.name.replace("-", "_")}
    unknown = [i for i in ids if i not in everything]
    if unknown:
        sys.exit(f"no unit in instances/: {', '.join(unknown)}")
    return {i: everything[i] for i in ids} if ids else everything


def _count(cfg, model, messages):
    body = client.build_body(cfg, model, messages, cfg["seeds"][0])
    body["options"]["num_predict"] = 1
    body["keep_alive"] = 0
    return client._post(cfg, "/api/chat", body, timeout=client.TIMEOUT_S)["prompt_eval_count"]


def _write(new_rows, columns):
    existing = {}
    if TABLE.exists():
        with open(TABLE, encoding="utf-8", newline="") as fh:
            existing = {r["id"]: r for r in csv.DictReader(fh)}
    existing.update({r["id"]: r for r in new_rows})
    with open(TABLE, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(existing[i] for i in sorted(existing))


def main(argv=None):
    p = argparse.ArgumentParser(description="Measures the prompt of each instance in each model.")
    p.add_argument("ids", nargs="*", help="instance ids (default: every one with a folder)")
    p.add_argument("--technique", default="few_shot", choices=prompts.TECHNIQUES)
    args = p.parse_args(argv)

    with open(ROOT / "config.yaml", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    limit = cfg["options"]["num_ctx"] - cfg["options"]["num_predict"]
    models = cfg["models"]
    units = _units(args.ids)

    version = None
    for m in models:
        version = client.environment(cfg, m)["ollama_version"]  # aborts if a digest changed

    columns = ["id", "smell", "technique", *(m["name"] for m in models),
               "largest", "limit", "fits", "date", "ollama"]
    rows = []
    for ident, unit in units.items():
        smell = unit.parent.parent.name
        messages = prompts.build(args.technique, smell, unit.read_text(encoding="utf-8"))
        counts = {m["name"]: _count(cfg, m, messages) for m in models}
        largest = max(counts.values())
        row = {"id": ident, "smell": smell, "technique": args.technique, **counts,
               "largest": largest, "limit": limit, "fits": "yes" if largest <= limit else "no",
               "date": datetime.date.today().isoformat(), "ollama": version}
        rows.append(row)
        # Writes after every instance: an interrupted run does not lose what it measured.
        _write([row], columns)
        print(f"{ident:8} {counts}  => {'fits' if largest <= limit else 'DOES NOT FIT'}", flush=True)

    not_fitting = [r["id"] for r in rows if r["fits"] == "no"]
    print(f"\ntable: {TABLE.relative_to(ROOT)}  (limit {limit} tokens)")
    if not_fitting:
        print(f"do not fit: {', '.join(not_fitting)}")
    return 1 if not_fitting else 0


if __name__ == "__main__":
    sys.exit(main())
