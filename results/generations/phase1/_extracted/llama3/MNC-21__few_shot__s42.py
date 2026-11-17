"""Code suggestions from an autocomplete service, read as a stream.

Public entry point: run(prompt, stops, suffix=""). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

from __future__ import annotations

import json
from contextlib import suppress
import requests

class CopilotResponse:
    def __init__(self, choices):
        self.choices = choices

class CopilotSuggestion:
    def __init__(self, text):
        self.text = text

def get_copilot_token():
    return "tok-123"

def get_suggestion(prompt: str, stops: list[str], suffix: str = "") -> str:
    payload = {
        "prompt": prompt,
        "suffix": suffix,
        "max_tokens": 200,
        "temperature": 0.8,
        "top_p": 1,
        "n": 1,
        "stop": stops,
        "stream": True,
        "extra": {
            "language": "python",
            "next_indent": 0,
            "trim_by_indentation": True,
        },
    }
    headers = {
        "OpenAI-Intent": "copilot-ghost",
        "OpenAI-Organization": "github-copilot",
        "Authorization": f"Bearer {get_copilot_token()}",
        "Content-Type": "application/json",
    }

    lines = []

    with requests.post(
        "https://copilot-proxy.githubusercontent.com/v1/engines/copilot-codex/completions",
        data=json.dumps(payload),
        headers=headers,
        stream=True,
    ) as resp:
        for line in resp.iter_lines():
            if line:
                line = line.decode("utf-8")[6:]  # Remove the data: prefix
                with suppress(json.JSONDecodeError):
                    response = json.loads(line)
                    if "choices" in response:
                        suggestion = CopilotSuggestion(response["choices"][0]["text"])
                        lines.append(suggestion.text)

    return "".join(lines)

def run(prompt, stops, suffix=""):
    """Requests the suggestion for the code snippet. Public entry point of this unit."""
    return get_suggestion(prompt, stops, suffix)
