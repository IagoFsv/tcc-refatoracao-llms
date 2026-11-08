from __future__ import annotations

import json
from contextlib import suppress
import requests

class SuggestionRequest:
    def __init__(self, prompt: str, stops: list[str], suffix: str = ""):
        self.prompt = prompt
        self.stops = stops
        self.suffix = suffix

    def get_temperature(self) -> float:
        line_count = self.prompt.count("\n")
        line_count = max(1, line_count - 2)
        if line_count <= 1:
            return 0
        elif line_count <= 10:
            return 0.2
        elif line_count < 20:
            return 0.4
        else:
            return 0.8

    def get_next_indent(self) -> int:
        # TODO: Calculate next indent
        return 0

    def get_extra(self) -> dict:
        return {
            "language": "python",
            "next_indent": self.get_next_indent(),
            "trim_by_indentation": True,
        }

    def get_payload(self) -> str:
        return json.dumps({
            "prompt": self.prompt,
            "suffix": self.suffix,
            "max_tokens": 200,
            "temperature": self.get_temperature(),
            "top_p": 1,
            "n": 1,
            # "logprobs": 0,
            "stop": self.stops,
            "stream": True,  # The API must be called with stream=True
            # "feature_flags": ["trim_to_block"],
            "extra": self.get_extra(),
        })

    def get_headers(self) -> dict:
        return {
            "OpenAI-Intent": "copilot-ghost",
            "OpenAI-Organization": "github-copilot",
            "Authorization": f"Bearer {get_copilot_token()}",
            "Content-Type": "application/json",
        }

    def execute(self) -> str:
        lines = []

        with requests.post(
            "https://copilot-proxy.githubusercontent.com/v1/engines/copilot-codex/completions",
            data=self.get_payload(),
            headers=self.get_headers(),
            stream=True,
        ) as resp:
            for line in resp.iter_lines():
                if line:
                    line = line.decode("utf-8")[6:]  # Remove the data: prefix
                    with suppress(json.JSONDecodeError):
                        lines.append(json.loads(line)["choices"][0]["text"])

        return "".join(lines)


def executar(prompt, stops, suffix=""):
    """Pede a sugestao para o trecho de codigo. Ponto de entrada publico desta unidade."""
    return SuggestionRequest(prompt, stops, suffix).execute()
