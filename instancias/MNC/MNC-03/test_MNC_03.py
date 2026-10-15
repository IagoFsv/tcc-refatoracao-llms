"""Testes da instancia MNC-03: fixam o comportamento observavel de executar().

So executar() e importado. O servico de completar texto e imitado na
unidade: executar recebe as escolhas que o servico devolveria e devolve o
resumo e os pedidos feitos (chave usada e parametros). A refatoracao pode
reorganizar o acesso a resposta; o que nao pode mudar e o pedido (chave lida
de OPENAI_API_KEY, modelo e parametros), o resumo (primeira escolha, sem
espacos e quebras de linha nas pontas) e o erro quando nao vem escolha.
"""

import pytest

from MNC_03 import executar

PARAMETROS = {
    "model": "text-davinci-002",
    "temperature": 0.7,
    "max_tokens": 256,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}


def test_tipico_primeira_escolha_sem_espacos_nas_pontas(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "chave-teste")

    resumo, pedidos = executar("Texto longo sobre clima.", ["\n\nResumo curto.\n", "Outra escolha"])

    assert resumo == "Resumo curto."
    assert pedidos == [("chave-teste", dict(PARAMETROS, prompt="Texto longo sobre clima."))]


def test_borda_tab_preservado_e_chave_ausente(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    resumo, pedidos = executar("", [" \n\tResumo\t \n "])

    assert resumo == "\tResumo\t"  # so espaco e quebra de linha saem das pontas
    assert pedidos == [(None, dict(PARAMETROS, prompt=""))]


def test_invalido_resposta_sem_escolhas(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "chave-teste")

    with pytest.raises(IndexError):
        executar("Texto", [])
