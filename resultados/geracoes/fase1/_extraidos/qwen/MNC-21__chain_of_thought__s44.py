from __future__ import annotations

import json
from contextlib import suppress

import requests


def get_copilot_token():
    """Token de acesso ao servico (fixo nesta unidade)."""
    return "tok-123"


def get_temperature(line_count):
    line_count = max(1, line_count - 2)
    if line_count <= 1:
        return 0
    elif line_count <= 10:
        return 0.2
    elif line_count < 20:
        return 0.4
    else:
        return 0.8


def create_payload(prompt: str, suffix: str, stops: list[str]) -> str:
    return json.dumps(
        {
            "prompt": prompt,
            "suffix": suffix,
            "max_tokens": 200,
            "temperature": get_temperature(prompt.count("\n")),
            "top_p": 1,
            "n": 1,
            "stop": stops,
            "stream": True,
            "extra": {
                "language": "python",
                "next_indent": 0,
                "trim_by_indentation": True,
            },
        },
    )


def parse_response(lines: list[str]) -> str:
    parsed_lines = []
    for line in lines:
        if line:
            line = line.decode("utf-8")[6:]  # Remove the data: prefix
            with suppress(json.JSONDecodeError):
                parsed_lines.append(json.loads(line)["choices"][0]["text"])
    return "".join(parsed_lines)


def get_suggestion(prompt: str, stops: list[str], suffix: str = "") -> str:
    if suffix:
        stops += (["def ", "class ", "if ", "\n#"],)

    payload = create_payload(prompt, suffix, stops)

    headers = {
        "OpenAI-Intent": "copilot-ghost",
        "OpenAI-Organization": "github-copilot",
        "Authorization": f"Bearer {get_copilot_token()}",
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
            lines.append(line)

    return parse_response(lines)


def executar(prompt, stops, suffix=""):
    """Pede a sugestao para o trecho de codigo. Ponto de entrada publico desta unidade."""
    return get_suggestion(prompt, stops, suffix)
