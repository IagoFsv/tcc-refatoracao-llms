"""
Client of the local models (Ollama) and recording of the generations.

Uses the native POST /api/chat endpoint, not the OpenAI-compatible /v1,
because only the native one accepts num_ctx and the other llama.cpp
"options". No system message is sent: each model receives the default SYSTEM
of its Modelfile, recorded by environment().

record() writes the raw output completely and immutably. That record is what
backs reproducibility and traceability: every number in the analysis must be
traceable to the exact call that produced it.
"""

import datetime
import json
import os
import time
from pathlib import Path

import requests

# A long generation on a modest GPU (with DeepSeek partly on the CPU) can
# take minutes; the limit only exists so the run never hangs forever.
TIMEOUT_S = 1800


def _url(cfg, path):
    return cfg["ollama"]["base_url"].rstrip("/") + path


def _get(cfg, path):
    r = requests.get(_url(cfg, path), timeout=30)
    r.raise_for_status()
    return r.json()


def _post(cfg, path, body, timeout=30):
    r = requests.post(_url(cfg, path), json=body, timeout=timeout)
    if not r.ok:
        # Ollama explains the error in the body (e.g. prompt larger than num_ctx).
        raise RuntimeError(f"HTTP {r.status_code} on {path}: {r.text}")
    return r.json()


def environment(cfg, model):
    """Describes the installed model and checks its digest against the config.

    Call once per run, before generating. Returns the Ollama version, digest,
    details, Modelfile, template, SYSTEM and Modelfile parameters. Raises
    RuntimeError if the tag is not installed or if the installed digest
    differs from config.yaml.
    """
    version = _get(cfg, "/api/version")["version"]
    installed = {m["name"]: m for m in _get(cfg, "/api/tags")["models"]}
    if model["tag"] not in installed:
        raise RuntimeError(
            f"{model['tag']} is not installed in Ollama "
            f"(ollama pull {model['tag']})."
        )
    digest = installed[model["tag"]]["digest"]
    if digest != model["digest"]:
        raise RuntimeError(
            f"Digest of {model['tag']} differs from config.yaml: "
            f"installed {digest}, expected {model['digest']}."
        )
    show = _post(cfg, "/api/show", {"model": model["tag"]})
    return {
        "ollama_version": version,
        "tag": model["tag"],
        "digest": digest,
        "details": show.get("details"),
        "modelfile": show.get("modelfile"),
        "template": show.get("template"),
        "system": show.get("system"),
        "modelfile_parameters": show.get("parameters"),
    }


def build_body(cfg, model, messages, seed):
    """Body of POST /api/chat: options from the config plus the seed of the run."""
    return {
        "model": model["tag"],
        "messages": messages,
        "stream": False,
        "options": {**cfg["options"], "seed": seed},
        **cfg["request"],
    }


def gpu_usage(cfg, model):
    """Fraction of the model loaded on the GPU, read from GET /api/ps.

    Call right after a generation, with the model still loaded. It only
    affects speed, not the result; it is recorded to document when part of
    the model runs on the CPU.
    """
    for m in _get(cfg, "/api/ps")["models"]:
        if m["name"] == model["tag"]:
            return {
                "size": m.get("size"),
                "size_vram": m.get("size_vram"),
                "gpu_fraction": round(m["size_vram"] / m["size"], 3)
                if m.get("size") else None,
                "context_length": m.get("context_length"),
            }
    return None


def call_model(cfg, model, messages, seed):
    """Makes one chat call and returns (text, body, raw_response, latency_s)."""
    body = build_body(cfg, model, messages, seed)
    start = time.time()
    response = _post(cfg, "/api/chat", body, timeout=TIMEOUT_S)
    latency = time.time() - start
    return response["message"]["content"], body, response, latency


def record(output_dir, identifier, cfg, model, env, body,
           raw_response, text, latency, gpu=None, extra=None):
    """Writes a JSON with all the metadata of the call.

    Keeps: tag and digest, Ollama version, endpoint, body sent (full prompt,
    options with seed, truncate/shift), UTC timestamp, latency, done_reason,
    token counts, GPU usage, text and the whole raw response, plus the fields
    in `extra` (instance, technique, seed, commit...). Never overwrites: if
    the file already exists, raises FileExistsError. Writes to a .tmp first
    and only then renames, so an interruption in the middle of writing does
    not leave a half-written JSON under the final name.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    entry = {
        "identifier": identifier,
        **(extra or {}),
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "model": model["name"],
        "tag": model["tag"],
        "digest": env["digest"],
        "ollama_version": env["ollama_version"],
        "endpoint": _url(cfg, "/api/chat"),
        "request": body,
        "latency_s": round(latency, 3),
        "done_reason": raw_response.get("done_reason"),
        "prompt_eval_count": raw_response.get("prompt_eval_count"),
        "eval_count": raw_response.get("eval_count"),
        "gpu_usage": gpu,
        "response_text": text,
        "raw_response": raw_response,
    }
    target = Path(output_dir) / f"{identifier}.json"
    if target.exists():
        raise FileExistsError(target)
    tmp = target.with_name(target.name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False, indent=2)
    os.replace(tmp, target)
    return target


def record_environment(output_dir, environments):
    """Writes the environment of the run (one item per model), without overwriting."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    target = Path(output_dir) / "_environment.json"
    with open(target, "x", encoding="utf-8") as f:
        json.dump(environments, f, ensure_ascii=False, indent=2)
    return target
