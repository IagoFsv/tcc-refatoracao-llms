from __future__ import annotations

import json
from contextlib import suppress
import requests

import os

def get_copilot_token() -> str:
    return "tok-123"

class SuggestionService:
    def __init__(self, token: str):
        self.token = token

    def get_suggestion(self, prompt: str, stops: list[str], suffix: str = "") -> str:
        payload = self._build_payload(prompt, stops, suffix)
        headers = self._build_headers()
        return self._make_request(payload, headers)

    def _build_payload(self, prompt: str, stops: list[str], suffix: str = "") -> str:
        line_count = prompt.count("\n")
        temperature = self._calculate_temperature(line_count)
        return json.dumps({
            "prompt": prompt,
            "suffix": suffix,
            "max_tokens": 200,
            "temperature": temperature,
            "top_p": 1,
            "n": 1,
            "stop": stops,
            "stream": True,
            "extra": {
                "language": "python",
                "next_indent": 0,
                "trim_by_indentation": True,
            },
        })

    def _build_headers(self) -> dict:
        return {
            "OpenAI-Intent": "copilot-ghost",
            "OpenAI-Organization": "github-copilot",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _make_request(self, payload: str, headers: dict) -> str:
        with requests.post(
            "https://copilot-proxy.githubusercontent.com/v1/engines/copilot-codex/completions",
            data=payload,
            headers=headers,
            stream=True,
        ) as resp:
            lines = []
            for line in resp.iter_lines():
                if line:
                    line = line.decode("utf-8")[6:]  # Remove the data: prefix
                    with suppress(json.JSONDecodeError):
                        lines.append(json.loads(line)["choices"][0]["text"])
            return "".join(lines)

def executar(prompt, stops, suffix=""):
    return SuggestionService(get_copilot_token()).get_suggestion(prompt, stops, suffix)
