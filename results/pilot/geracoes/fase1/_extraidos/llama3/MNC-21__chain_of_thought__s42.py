from __future__ import annotations

import json
from contextlib import suppress

import requests


def get_copilot_token():
    """Token de acesso ao servico (fixo nesta unidade)."""
    return "tok-123"


def get_suggestion(prompt: str, stops: list[str], suffix: str = "") -> str:
    """
    Get a suggestion from GitHub Copilot
    """

    def calculate_temperature(line_count):
        if line_count <= 1:
            return 0
        elif line_count <= 10:
            return 0.2
        elif line_count < 20:
            return 0.4
        else:
            return 0.8

    if suffix:
        stops += (["def ", "class ", "if ", "\n#"],)

    payload = json.dumps(
        {
            # ...
        }
    )

    # ...

    return "".join(lines)

def get_temperature(line_count):
    return calculate_temperature(line_count)

def executar(prompt, stops, suffix=""):
    """Pede a sugestao para o trecho de codigo. Ponto de entrada publico desta unidade."""
    return get_suggestion(prompt, stops, suffix)
