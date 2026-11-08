from __future__ import annotations

import json
from contextlib import suppress

import requests


class CopilotService:
    def __init__(self):
        self.token = self.get_copilot_token()
        self.headers = self.get_headers()

    def get_copilot_token(self) -> str:
        """Token de acesso ao servico  (fixo nesta unidade)."""
        return "tok-123"

    def get_headers(self) -> dict:
        """Headers para a requisição."""
        return {
            "OpenAI-Intent": "copilot-ghost",
            "OpenAI-Organization": "github-copilot",
            "Authorization": f"Bearer {self.get_copilot_token()}",
            "Content-Type": "application/json",
        }

    def get_temperature(self, line_count: int) -> float:
        """Calcula a temperatura baseado na contagem de linhas."""
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
        """
        Get a suggestion from GitHub Copilot
        """
        payload = self.get_payload(prompt, stops, suffix)

        lines = self.get_response(payload)

        return "".join(lines)

    def get_payload(self, prompt: str, stops: list[str], suffix: str = "") -> str:
        """Monta o payload da requisição."""
        return json.dumps(
            {
                "prompt": prompt,
                "suffix": suffix,
                "max_tokens": 200,
                "temperature": self.get_temperature(prompt.count("\n")),
                "top_p": 1,
                "n": 1,
                "stream": True,
                "extra": {
                    "language": "python",
                    "next_indent": 0,
                    "trim_by_indentation": True,
                },
            },
        )

    def get_response(self, payload: str) -> list[str]:
        """Faz a requisição e retorna as respostas."""
        lines = []

        with requests.post(
            "https://copilot-proxy.githubusercontent.com/v1/engines/copilot-codex/completions",
            data=payload,
            headers=self.headers,
            stream=True,
        ) as resp:
            for line in resp.iter_lines():
                if line:
                    line = line.decode("utf-8")[6:]
                    with suppress(json.JSONDecodeError):
                        lines.append(json.loads(line)["choices"][0]["text"])

        return lines


def executar(prompt, stops, suffix=""):
    """Pede a sugestao para o trecho de codigo. Ponto de entrada publico desta unidade."""
    copilot_service = CopilotService()
    return copilot_service.get_suggestion(prompt, stops, suffix)
