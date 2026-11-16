from __future__ import annotations

import json
from contextlib import suppress
import requests

class CopilotService:
    def __init__(self, token: str):
        self.token = token

    def get_suggestion(self, prompt: str, stops: list[str], suffix: str = "") -> str:
        payload = json.dumps({
            "prompt": prompt,
            "suffix": suffix,
            "max_tokens": 200,
            "temperature": self.calculate_temperature(prompt.count("\n")),
            "top_p": 1,
            "n": 1,
            # "logprobs": 0,
            "stop": stops,
            "stream": True,  # The API must be called with stream=True
            # "feature_flags": ["trim_to_block"],
            "extra": {
                "language": "python",
                "next_indent": 0,
                "trim_by_indentation": True,
            },
        })
        headers = {
            "OpenAI-Intent": "copilot-ghost",
            "OpenAI-Organization": "github-copilot",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        lines = []

        with requests.post(
            "https://copilot-proxy.githubusercontent.com/v1/engines/copilot-codex/completions",
            data=payload,
            headers=headers,
            stream=True,
        ) as resp:
            for line in resp.iter_lines():
                if line:
                    line = line.decode("utf-8")[6:]  # Remove the data: prefix
                    with suppress(json.JSONDecodeError):
                        lines.append(json.loads(line)["choices"][0]["text"])

        return "".join(lines)

    def calculate_temperature(self, line_count: int) -> float:
        line_count = max(1, line_count - 2)
        if line_count <= 1:
            return 0
        elif line_count <= 10:
            return 0.2
        elif line_count < 20:
            return 0.4
        else:
            return 0.8

def executar(prompt: str, stops: list[str], suffix: str = "") -> str:
    """Pede a sugestao para o trecho de codigo. Ponto de entrada publico desta unidade."""
    service = CopilotService(get_copilot_token())
    return service.get_suggestion(prompt, stops, suffix)
