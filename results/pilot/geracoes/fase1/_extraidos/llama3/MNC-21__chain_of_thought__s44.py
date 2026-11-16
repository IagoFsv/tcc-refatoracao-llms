from __future__ import annotations

import json
from contextlib import suppress

import requests


def get_copilot_token():
    """Token de acesso ao servico (fixo nesta unidade)."""
    return "tok-123"


def get_temperature(line_count):
    if line_count <= 1:
        return 0
    elif line_count <= 10:
        return 0.2
    elif line_count < 20:
        return 0.4
    else:
        return 0.8

def build_payload(prompt: str, stops: list[str], suffix: str = "") -> dict:
    line_count = prompt.count("\n")
    temperature = get_temperature(line_count)
    payload = {
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
    }
    return payload

def get_suggestion(prompt: str, stops: list[str], suffix: str = "") -> str:
    payload = build_payload(prompt, stops, suffix)
    # ...

def executar(prompt, stops, suffix=""):
    """Pede a sugestao para o trecho de codigo. Ponto de entrada publico desta unidade."""
    return get_suggestion(prompt, stops, suffix)
