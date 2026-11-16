"""
Generation loop (step 4): each instance -> 3 models -> 3 techniques -> 3
runs, one independent call (fresh context) per combination.

Ordered in layers, one per seed (runs 1, 2 and 3). Each layer covers every
instance, model and technique, so stopping in the middle of the run leaves
complete, balanced layers, and never a whole model without output. Within a
layer, one model at a time (with 8 GB of VRAM only one fits loaded, and
alternating would make Ollama reload at every call); within it, instance and
technique. Each call becomes an immutable JSON at
results/generations/<phase>/<model>/<ID>__<technique>__s<seed>.json.

Resumable: whatever already has a record is skipped, so it is enough to run
again after an interruption. Nothing is generated again because the output
was bad: bad output is data. A call that fails because of infrastructure
(HTTP, timeout, Ollama down) produces no record, goes to the errors.jsonl of
the session and is redone next time. done_reason "length" (truncated output)
is recorded like any other and only counted separately.

Locks, so every generation sees the same instrument:
  - clean git tree outside results/, and the commit goes into every record;
  - Ollama version equal to config.yaml and model digest equal to the
    config, checked before every call;
  - one run at a time (_running.lock file in the phase folder).

The refactored code is NOT extracted here: the raw response stays untouched
and extraction is a separate step.

Usage:
    python -m generation.generate --dry-run      # checks everything and counts what is missing
    python -m generation.generate --pilot        # LM-01, LPL-01, LLF-01, MNC-01, first seed,
                                                 # in _pilot/ (disposable, outside git)
    python -m generation.generate                # whole phase, resumes where it stopped
    python -m generation.generate --model qwen   # one model only
"""

import argparse
import datetime
import json
import os
import statistics
import subprocess
import sys
from pathlib import Path

# Same reason as in smoke_test: the Windows console breaks on characters
# outside its code page.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import requests
import yaml
from tqdm import tqdm

from generation import client, prompts

ROOT = Path(__file__).resolve().parents[1]
INSTANCES = ROOT / "instances"
GENERATIONS = ROOT / "results" / "generations"
PHASE = "phase1"

# Pilot: only measures time and tests the pipeline.
PILOT_IDS = ("LM-01", "LPL-01", "LLF-01", "MNC-01")

# Consecutive infrastructure failures before giving up (Ollama down).
MAX_CONSECUTIVE_FAILURES = 3


def _units(ids=None):
    """{id: unit path} of the instances that have a folder (or only the requested ones)."""
    everything = {p.parent.name: p for p in sorted(INSTANCES.glob("*/*/*.py"))
                  if p.stem == p.parent.name.replace("-", "_")}
    if not ids:
        return everything
    unknown = [i for i in ids if i not in everything]
    if unknown:
        sys.exit(f"no unit in instances/: {', '.join(unknown)}")
    return {i: everything[i] for i in ids}


def _git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout.strip()


def _commit(require_clean):
    """HEAD hash. Aborts if there are changes outside results/ (when required)."""
    dirty = _git("status", "--porcelain", "--", ".", ":(exclude)results")
    if dirty and require_clean:
        sys.exit("There are uncommitted changes outside results/. Commit before "
                 "generating, so every record points to the exact version of "
                 "what went into the prompt:\n" + dirty)
    return _git("rev-parse", "HEAD") + ("-dirty" if dirty else "")


def _check_instrument(cfg, model):
    """Aborts if the Ollama version or the model digest changed.

    Called before every generation: the Ollama app may update itself and an
    `ollama pull` may swap the model in the middle of the run. A connection
    error propagates as requests.RequestException (infrastructure failure).
    """
    version = client._get(cfg, "/api/version")["version"]
    if version != cfg["ollama"]["version"]:
        sys.exit(f"Ollama {version} installed, config.yaml expects "
                 f"{cfg['ollama']['version']}. Run interrupted.")
    installed = {m["name"]: m["digest"] for m in client._get(cfg, "/api/tags")["models"]}
    if installed.get(model["tag"]) != model["digest"]:
        sys.exit(f"Digest of {model['tag']} changed (installed "
                 f"{installed.get(model['tag'])}). Run interrupted.")


def _tasks(models, units, seeds, phase_dir):
    """Every combination, in execution order, with the target of its record."""
    for run, seed in enumerate(seeds, start=1):
        for m in models:
            for ident, unit in units.items():
                for technique in prompts.TECHNIQUES:
                    target = phase_dir / m["name"] / f"{ident}__{technique}__s{seed}.json"
                    yield m, ident, unit, technique, run, seed, target


def _record_failure(session_dir, task, error):
    m, ident, _, technique, _, seed, _ = task
    line = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "model": m["name"], "instance": ident, "technique": technique,
            "seed": seed, "error": f"{type(error).__name__}: {error}"}
    with open(session_dir / "errors.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(line, ensure_ascii=False) + "\n")


def main(argv=None):
    p = argparse.ArgumentParser(description="Generation loop.")
    p.add_argument("--pilot", action="store_true",
                   help=f"only {', '.join(PILOT_IDS)} with the first seed, in _pilot/")
    p.add_argument("--model", action="append",
                   help="only this model (name in config.yaml); may be repeated")
    p.add_argument("--dry-run", action="store_true",
                   help="check the environment and count what is missing, without generating")
    args = p.parse_args(argv)

    with open(ROOT / "config.yaml", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    models = cfg["models"]
    if args.model:
        unknown = set(args.model) - {m["name"] for m in models}
        if unknown:
            sys.exit(f"model not in config.yaml: {', '.join(sorted(unknown))}")
        models = [m for m in models if m["name"] in args.model]

    session = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    if args.pilot:
        units = _units(PILOT_IDS)
        seeds = cfg["seeds"][:1]
        phase_dir = GENERATIONS / "_pilot" / session
    else:
        units = _units()
        seeds = cfg["seeds"]
        phase_dir = GENERATIONS / PHASE
    commit = _commit(require_clean=not (args.pilot or args.dry_run))

    # Full environment of every model at the start: if a digest does not
    # match, stop before generating anything.
    environments = {}
    try:
        for m in models:
            _check_instrument(cfg, m)
            environments[m["name"]] = client.environment(cfg, m)
    except requests.RequestException:
        sys.exit(f"Ollama is down at {cfg['ollama']['base_url']}. Open Ollama and run again.")

    tasks = list(_tasks(models, units, seeds, phase_dir))
    pending = [t for t in tasks if not t[-1].exists()]
    print(f"{len(units)} instances x {len(models)} models x "
          f"{len(prompts.TECHNIQUES)} techniques x {len(seeds)} seeds = {len(tasks)} calls")
    for run, seed in enumerate(seeds, start=1):
        per_model = ", ".join(f"{m['name']} {sum(t[0] is m and t[5] == seed for t in pending)}"
                              for m in models)
        print(f"  layer {run} (seed {seed}) pending: {per_model}")
    print(f"commit {commit}, Ollama {cfg['ollama']['version']}, target "
          f"{phase_dir.relative_to(ROOT)}")
    if commit.endswith("-dirty") and not args.pilot:
        print("WARNING: there are uncommitted changes; the real run will refuse.")
    if args.dry_run or not pending:
        return 0

    phase_dir.mkdir(parents=True, exist_ok=True)
    lock = phase_dir / "_running.lock"
    try:
        with open(lock, "x", encoding="utf-8") as fh:
            fh.write(f"pid {os.getpid()}, session {session}\n")
    except FileExistsError:
        sys.exit(f"{lock.relative_to(ROOT)} already exists: another run in progress? "
                 "If none is running (the previous one was killed), delete the "
                 "file and run again.")

    session_dir = phase_dir / "_sessions" / session
    done, truncated, failures, consecutive = 0, [], 0, 0
    latencies = {m["name"]: [] for m in models}
    try:
        session_dir.mkdir(parents=True)
        with open(session_dir / "_environment.json", "x", encoding="utf-8") as fh:
            json.dump({"session": session, "commit": commit, "pilot": args.pilot,
                       "python": sys.version, "argv": sys.argv[1:],
                       "models": list(environments.values())}, fh, ensure_ascii=False, indent=2)

        for task in tqdm(pending, unit="call", dynamic_ncols=True):
            m, ident, unit, technique, run, seed, target = task
            smell = unit.parent.parent.name
            messages = prompts.build(technique, smell, unit.read_text(encoding="utf-8"))
            try:
                _check_instrument(cfg, m)
                text, body, raw, latency = client.call_model(cfg, m, messages, seed)
                gpu = client.gpu_usage(cfg, m)
            except (requests.RequestException, RuntimeError) as e:
                failures += 1
                consecutive += 1
                _record_failure(session_dir, task, e)
                tqdm.write(f"[failure] {m['name']} {target.stem}: {type(e).__name__}: {e}")
                if consecutive >= MAX_CONSECUTIVE_FAILURES:
                    sys.exit(f"{consecutive} consecutive failures: is Ollama up? "
                             "Run again to resume.")
                continue
            consecutive = 0
            client.record(target.parent, target.stem, cfg, m, environments[m["name"]],
                          body, raw, text, latency, gpu,
                          extra={"instance": ident, "smell": smell, "technique": technique,
                                 "run": run, "seed": seed,
                                 "commit": commit, "session": session})
            done += 1
            latencies[m["name"]].append(latency)
            if raw.get("done_reason") != "stop":
                truncated.append(target.stem)
                tqdm.write(f"[warning] {m['name']} {target.stem}: "
                           f"done_reason={raw.get('done_reason')}")
    finally:
        lock.unlink(missing_ok=True)

    print(f"\ndone {done}, failures {failures} (in {session_dir.relative_to(ROOT)}/errors.jsonl), "
          f"done_reason != stop: {len(truncated)}")
    # Estimate for the whole phase, useful mainly in the pilot.
    per_model = len(_units()) * len(prompts.TECHNIQUES) * len(cfg["seeds"])
    for name, lats in latencies.items():
        if lats:
            mean = statistics.mean(lats)
            print(f"  {name:9} mean {mean:.1f} s/call; whole phase ({per_model} "
                  f"calls) ~ {mean * per_model / 3600:.1f} h")
    remaining = sum(not t[-1].exists() for t in tasks)
    if remaining:
        print(f"{remaining} remaining: run again to resume.")
    return 1 if remaining else 0


if __name__ == "__main__":
    sys.exit(main())
