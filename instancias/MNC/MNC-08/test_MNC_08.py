"""Testes da instancia MNC-08: fixam o comportamento observavel de executar().

So executar() e importado. O servico de completar texto e imitado na
unidade: executar recebe as escolhas que o servico devolveria e devolve a
resposta e os pedidos feitos (chave usada e parametros). A refatoracao pode
reorganizar o acesso a resposta; o que nao pode mudar e o pedido (chave lida
de OPENAI_API_KEY, modelo e parametros), a resposta (primeira escolha, sem
espacos e quebras de linha nas pontas) e o erro quando nao vem escolha.
"""

import pytest

from MNC_08 import executar

PARAMETROS = {
    "temperature": 0,
    "max_tokens": 300,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "model": "text-davinci-003",
}


def test_tipico_primeira_escolha_sem_espacos_nas_pontas(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "chave-teste")

    resposta, pedidos = executar("Qual a capital da Noruega?", ["\n\nOslo.\n", "Bergen"])

    assert resposta == "Oslo."
    assert pedidos == [("chave-teste", dict(PARAMETROS, prompt="Qual a capital da Noruega?"))]


def test_borda_tab_preservado_e_chave_ausente(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    resposta, pedidos = executar("", [" \n\tOslo\t \n "])

    assert resposta == "\tOslo\t"  # so espaco e quebra de linha saem das pontas
    assert pedidos == [(None, dict(PARAMETROS, prompt=""))]


def test_invalido_resposta_sem_escolhas(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "chave-teste")

    with pytest.raises(IndexError):
        executar("Pergunta", [])
