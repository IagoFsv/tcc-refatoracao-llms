"""Code suggestions from an autocomplete service, read as a stream.

Public entry point: run(prompt, stops, suffix=""). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

from __future__ import annotations

import json
from contextlib import suppress

import requests


class CopilotToken:
    """Access token of the service (fixed in this unit)."""

    @staticmethod
    def get_token():
        return "tok-123"


class SuggestionRequest:
    """Request for a suggestion from GitHub Copilot."""

    def __init__(self, prompt: str, stops: list[str], suffix: str = ""):
        self.prompt = prompt
        self.stops = stops
        self.suffix = suffix

    def get_payload(self):
        line_count = self.prompt.count("\n")
        line_count = max(1, line_count - 2)
        temperature = 0
        if line_count <= 1:
            temperature = 0
        elif line_count <= 10:
            temperature = 0.2
        elif line_count < 20:
            temperature = 0.4
        else:
            temperature = 0.8

        if self.suffix:
            self.stops += (["def ", "class ", "if ", "\n#"],)

        return {
            "prompt": self.prompt,
            "suffix": self.suffix,
            "max_tokens": 200,
            "temperature": temperature,
            "top_p": 1,
            "n": 1,
            "stop": self.stops,
            "stream": True,
            "extra": {
                "language": "python",
                "next_indent": 0,
                "trim_by_indentation": True,
            },
        }

    def get_headers(self):
        return {
            "OpenAI-Intent": "copilot-ghost",
            "OpenAI-Organization": "github-copilot",
            "Authorization": f"Bearer {CopilotToken.get_token()}",
            "Content-Type": "application/json",
        }


class SuggestionResponse:
    """Response from GitHub Copilot."""

    @staticmethod
    def parse_line(line):
        line = line.decode("utf-8")[6:]
        try:
            return json.loads(line)["choices"][0]["text"]
        except json.JSONDecodeError:
            return None


class CopilotClient:
    """Client for the GitHub Copilot API."""

    @staticmethod
    def send_request(request: SuggestionRequest):
        payload = request.get_payload()
        headers = request.get_headers()

        with requests.post(
            "https://copilot-proxy.githubusercontent.com/v1/engines/copilot-codex/completions",
            data=json.dumps(payload),
            headers=headers,
            stream=True,
        ) as resp:
            lines = []
            for line in resp.iter_lines():
                if line:
                    parsed_line = SuggestionResponse.parse_line(line)
                    if parsed_line:
                        lines.append(parsed_line)
            return "".join(lines)


def get_suggestion(prompt: str, stops: list[str], suffix: str = "") -> str:
    """
    Get a suggestion from GitHub Copilot
    """
    request = SuggestionRequest(prompt, stops, suffix)
    return CopilotClient.send_request(request)


def run(prompt, stops, suffix=""):
    """Requests the suggestion for the code snippet. Public entry point of this unit."""
    return get_suggestion(prompt, stops, suffix)
