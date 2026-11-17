"""Code suggestions from an autocomplete service, read as a stream.

Public entry point: run(prompt, stops, suffix=""). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

from __future__ import annotations

import json
from contextlib import suppress
from typing import List

import requests
from dataclasses import dataclass, field


def get_copilot_token():
    """Access token of the service  (fixed in this unit)."""
    return "tok-123"


@dataclass
class Extra:
    language: str = "python"
    next_indent: int = 0
    trim_by_indentation: bool = True


@dataclass
class Payload:
    prompt: str
    suffix: str = ""
    max_tokens: int = 200
    temperature: float = 0.0
    top_p: float = 1.0
    n: int = 1
    stream: bool = True  
    extra: Extra = field(default_factory=Extra)


@dataclass
class Response:
    choices: List[dict] = field(default_factory=list)


def get_temperature(line_count):
    line_count = max(1, line_count - 2)
    if line_count <= 1:
        return 0.0
    elif line_count <= 10:
        return 0.2
    elif line_count < 20:
        return 0.4
    else:
        return 0.8


def get_suggestion(prompt: str, stops: List[str], suffix: str = "") -> str:
    """
    Get a suggestion from GitHub Copilot
    """
    payload = Payload(
        prompt=prompt,
        suffix=suffix,
        temperature=get_temperature(prompt.count("\n")),
    )
    headers = {
        "OpenAI-Intent": "copilot-ghost",
        "OpenAI-Organization": "github-copilot",
        "Authorization": f"Bearer {get_copilot_token()}",
        "Content-Type": "application/json",
    }

    lines = []

    with requests.post(
        "https://copilot-proxy.githubusercontent.com/v1/engines/copilot-codex/completions",
        data=json.dumps(payload.__dict__),
        headers=headers,
        stream=True,
    ) as resp:
        for line in resp.iter_lines():
            if line:
                line = line.decode("utf-8")[6:]  
                with suppress(json.JSONDecodeError):
                    lines.append(json.loads(line)["choices"][0]["text"])

    return "".join(lines)


def run(prompt, stops, suffix=""):
    """Requests the suggestion for the code snippet. Public entry point of this unit."""
    return get_suggestion(prompt, stops, suffix)
