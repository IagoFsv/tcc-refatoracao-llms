"""Testes da instancia MNC-21: fixam o comportamento observavel de executar().

So executar() e importado. O teste intercepta requests.post com uma resposta
em fluxo gravada (linhas "data: {...}"). A refatoracao pode reorganizar a
montagem do pedido e a leitura do fluxo; o que nao pode mudar e o pedido
(URL, cabecalhos, corpo JSON, stream ligado), o texto devolvido (pedacos
juntados na ordem, linhas vazias e linhas que nao sao JSON ignoradas) e o
erro diante de pedaco sem choices.

Os testes fixam o comportamento como ele e, inclusive o defeito do original:
com suffix, a lista de paradas extras entra como um item so (uma lista dentro
de stops), nao como quatro paradas.
"""

import json

import pytest
import requests

from MNC_21 import executar

URL = "https://copilot-proxy.githubusercontent.com/v1/engines/copilot-codex/completions"
CABECALHOS = {
    "OpenAI-Intent": "copilot-ghost",
    "OpenAI-Organization": "github-copilot",
    "Authorization": "Bearer tok-123",
    "Content-Type": "application/json",
}


class RespostaEmFluxo:
    def __init__(self, linhas):
        self.linhas = linhas

    def __enter__(self):
        return self

    def __exit__(self, *erro):
        return False

    def iter_lines(self):
        return iter(self.linhas)


@pytest.fixture
def api(monkeypatch):
    """Intercepta requests.post; devolve (pedidos, fluxo)."""
    pedidos = []
    fluxo = []

    def falso_post(url, **kwargs):
        pedidos.append((url, kwargs))
        return RespostaEmFluxo(list(fluxo))

    monkeypatch.setattr(requests, "post", falso_post)
    return pedidos, fluxo


def pedaco(texto):
    return ("data: " + json.dumps({"choices": [{"text": texto, "index": 0}]})).encode("utf-8")


def corpo(prompt, suffix, temperatura, stops):
    return {
        "prompt": prompt,
        "suffix": suffix,
        "max_tokens": 200,
        "temperature": temperatura,
        "top_p": 1,
        "n": 1,
        "stop": stops,
        "stream": True,
        "extra": {"language": "python", "next_indent": 0, "trim_by_indentation": True},
    }


def test_tipico_pedacos_juntados_e_pedido_completo(api):
    pedidos, fluxo = api
    fluxo += [pedaco("return "), b"", pedaco("a + b"), b"data: [DONE]"]
    prompt = "def soma(a, b):\n    "

    assert executar(prompt, ["\n\n"]) == "return a + b"

    assert len(pedidos) == 1
    url, kwargs = pedidos[0]
    assert url == URL
    assert kwargs["headers"] == CABECALHOS
    assert kwargs["stream"] is True
    assert json.loads(kwargs["data"]) == corpo(prompt, "", 0, ["\n\n"])


def test_borda_suffix_temperatura_por_numero_de_linhas_e_fluxo_vazio(api):
    pedidos, fluxo = api

    assert executar("x = 1\n" * 12, ["\n"], suffix="fim") == ""
    for quebras in (3, 4, 13, 21, 22):  # linhas contadas = quebras - 2
        assert executar("x = 1\n" * quebras, []) == ""

    enviados = [json.loads(kwargs["data"]) for _, kwargs in pedidos]
    assert enviados[0] == corpo("x = 1\n" * 12, "fim", 0.2, ["\n", ["def ", "class ", "if ", "\n#"]])
    assert [e["temperature"] for e in enviados[1:]] == [0, 0.2, 0.4, 0.4, 0.8]


def test_invalido_pedaco_sem_choices(api):
    _, fluxo = api
    fluxo += [pedaco("ok"), b'data: {"error": "rate limited"}']

    with pytest.raises(KeyError):
        executar("def f():\n", [])
