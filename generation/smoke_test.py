"""
Smoke test: makes ONE short call to each model in the config and records the result.

Purpose: confirm that Ollama answers, that tags and digests match the config
and that recording works, before running the generation loop.

Usage:
    python -m generation.smoke_test            # calls the models for real
    python -m generation.smoke_test --dry-run  # generates no text: only checks
                                               # config, Ollama up and digests

Each run writes to results/generations/_smoke_test/<timestamp>/ (outside
version control), with the environment in _environment.json.
"""

import argparse
import datetime
import sys
from pathlib import Path

# The Windows console uses a code page by default (e.g. cp1252) that does not
# cover all of Unicode; if a model answer contains an emoji or another
# character outside that table, print() fails with UnicodeEncodeError even
# though the call and the record on disk (always UTF-8) worked.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import yaml

from generation import client

ROOT = Path(__file__).resolve().parents[1]

# No system message, as in the study: the default SYSTEM of the Modelfile applies.
TEST_PROMPT = [
    {"role": "user", "content": "Answer only with the word: OK"},
]


def load_config():
    with open(ROOT / "config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Smoke test of the local models.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Generate no text; only check config, Ollama and digests.")
    args = parser.parse_args()

    cfg = load_config()
    models = cfg["models"]
    seed = cfg["seeds"][0]
    run_id = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    log_dir = ROOT / "results" / "generations" / "_smoke_test" / run_id

    print(f"Testing {len(models)} model(s). dry-run={args.dry_run}")
    print(f"options: {cfg['options']} seed={seed}\n")
    failed = False
    environments = []

    for m in models:
        label = f"{m['name']} ({m['tag']})"
        try:
            env = client.environment(cfg, m)
        except Exception as e:  # noqa: BLE001 - any failure should be shown here
            failed = True
            print(f"[FAIL] {label}\n       {type(e).__name__}: {e}\n")
            continue
        environments.append(env)

        if args.dry_run:
            print(f"[dry-run] {label}")
            print(f"          Ollama {env['ollama_version']}, digest matches "
                  f"({env['digest'][:12]}), "
                  f"{env['details']['quantization_level']}\n")
            continue

        try:
            text, body, raw, latency = client.call_model(cfg, m, TEST_PROMPT, seed)
            gpu = client.gpu_usage(cfg, m)
            path = client.record(log_dir, m["name"], cfg, m, env, body, raw, text, latency, gpu)
            print(f"[ok] {label}  ({latency:.1f}s)")
            print(f"     answer: {text!r}")
            print(f"     done_reason={raw.get('done_reason')} "
                  f"prompt={raw.get('prompt_eval_count')} "
                  f"output={raw.get('eval_count')} tokens")
            if gpu:
                print(f"     GPU: {gpu['gpu_fraction']:.0%} "
                      f"(context_length={gpu['context_length']})")
            print(f"     record: {path.relative_to(ROOT)}\n")
        except Exception as e:  # noqa: BLE001
            failed = True
            print(f"[FAIL] {label}\n       {type(e).__name__}: {e}\n")

    if environments and not args.dry_run:
        client.record_environment(log_dir, environments)

    if failed:
        print("One or more models failed. Check Ollama and config.yaml.")
        sys.exit(1)

    if not args.dry_run:
        print("All models answered. Ollama wiring confirmed.")


if __name__ == "__main__":
    main()
