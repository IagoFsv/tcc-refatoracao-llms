from __future__ import annotations

import json
from contextlib import suppress
import requests

class GitHubCopilot:
    """Token de acesso ao servico (fixo nesta unidade)."""
    token = "tok-123"

    def __init__(self):
        pass

    def get_temperature(self, line_count: int) -> float:
        """Calculate temperature"""
        line_count = max(1, line_count - 2)
        if line_count <= 1:
            return 0
        elif line_count <= 10:
            return 0.2
        elif line_count < 20:
            return 0.4
        else:
            return 0.8

    def get_suggestion(self, prompt: str, stops: list[str], suffix: str = "") -> str:
        """Get a suggestion from GitHub Copilot"""
        if suffix:
            stops += (["def ", "class ", "if ", "\n#"],)

        payload = json.dumps({
            "prompt": prompt,
            "suffix": suffix,
            "max_tokens": 200,
            "temperature": self.get_temperature(prompt.count("\n")),
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
            # The API returns a stream of JSON-like objects or blank lines
            # We need to parse the JSON-like objects and ignore the blank lines
            # The format of the JSON-like objects is:
            # data: {"choices": [{"text": "suggestion"}]}}

            for line in resp.iter_lines():
                if line:
                    line = line.decode("utf-8")[6:]  # Remove the data: prefix
                    with suppress(json.JSONDecodeError):
                        lines.append(json.loads(line)["choices"][0]["text"])

        return "".join(lines)

    def executar(self, prompt: str, stops: list[str], suffix: str = "") -> str:
        """Pede a sugestao para o trecho de codigo. Ponto de entrada publico desta unidade."""
        return self.get_suggestion(prompt, stops, suffix)
