from __future__ import annotations

import json
from contextlib import suppress
import requests

class CopilotConfig:
    def __init__(self):
        self.token = "tok-123"
        self.api_url = "https://copilot-proxy.githubusercontent.com/v1/engines/copilot-codex/completions"

    def get_temperature(self, line_count):
        line_count = max(1, line_count - 2)
        if line_count <= 1:
            return 0
        elif line_count <= 10:
            return 0.2
        elif line_count < 20:
            return 0.4
        else:
            return 0.8

    def get_payload(self, prompt: str, stops: list[str], suffix: str = "") -> str:
        if suffix:
            stops += (["def ", "class ", "if ", "\n#"],)
        payload = {
            "prompt": prompt,
            "suffix": suffix,
            "max_tokens": 200,
            "temperature": self.get_temperature(prompt.count("\n")),
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
        return json.dumps(payload)

    def get_headers(self) -> dict:
        return {
            "OpenAI-Intent": "copilot-ghost",
            "OpenAI-Organization": "github-copilot",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

def get_suggestion(prompt: str, stops: list[str], suffix: str = "", config: CopilotConfig = None) -> str:
    config = config or CopilotConfig()
    payload = config.get_payload(prompt, stops, suffix)
    headers = config.get_headers()

    lines = []

    with requests.post(config.api_url, data=payload, headers=headers, stream=True) as resp:
        for line in resp.iter_lines():
            if line:
                line = line.decode("utf-8")[6:]
                with suppress(json.JSONDecodeError):
                    lines.append(json.loads(line)["choices"][0]["text"])

    return "".join(lines)

def executar(prompt, stops, suffix=""):
    """Pede a sugestao para o trecho de codigo. Ponto de entrada publico desta unidade."""
    return get_suggestion(prompt, stops, suffix)
