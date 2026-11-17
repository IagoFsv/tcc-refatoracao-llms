"""Code suggestions from an autocomplete service, read as a stream.

Public entry point: run(prompt, stops, suffix=""). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

from __future__ import annotations

import json
from contextlib import suppress

import requests


def get_copilot_token():
    """Access token of the service (fixed in this unit)."""
    return "tok-123"


def get_suggestion(prompt: str, stops: list[str], suffix: str = "") -> str:
    """
    Get a suggestion from GitHub Copilot
    """

    def get_temperature(line_count):
        # ...

    if suffix:
        stops += (["def ", "class ", "if ", "\n#"],)

    # Create separate variables for each level of nesting
    extra = {"language": "python", "next_indent": 0, "trim_by_indentation": True}
    payload = json.dumps(
        {
            "prompt": prompt,
            "suffix": suffix,
            "max_tokens": 200,
            "temperature": get_temperature(prompt.count("\n")),
            "top_p": 1,
            "n": 1,
            "stop": stops,
            "stream": True,
            "extra": extra,
        }
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
        data=payload,
        headers=headers,
        stream=True,
    ) as resp:
        # ...
