"""Testes da instancia MNC-14: fixam o comportamento observavel de executar().

So executar() e importado. O teste intercepta requests.get com respostas
gravadas da API de bots (getUpdates e getFile). A refatoracao pode
reorganizar o acesso ao JSON e os lacos; o que nao pode mudar e a ordem dos
pedidos, a lista de caminhos devolvida (primeiro documentos de respostas,
depois documentos diretos, sem repetir) e o erro quando getFile nao traz o
resultado.
"""

import pytest
import requests

from MNC_14 import executar

URL = "https://api.telegram.org/bot{}/{}"


class Resposta:
    def __init__(self, dados):
        self.dados = dados

    def json(self):
        return self.dados


def documento(file_id):
    return {"document": {"file_id": file_id, "file_name": file_id + ".pdf"}}


def resposta_a(file_id):
    return {"message": {"reply_to_message": documento(file_id), "text": "veja"}}


def direto(file_id):
    return {"message": documento(file_id)}


@pytest.fixture
def api(monkeypatch):
    """Intercepta requests.get; devolve (pedidos, atualizacoes, caminhos)."""
    pedidos = []
    atualizacoes = []
    caminhos = {}

    def falso_get(url, *args, **kwargs):
        pedidos.append(url)
        if url.endswith("/getUpdates"):
            return Resposta({"ok": True, "result": atualizacoes})
        file_id = url.split("file_id=")[1]
        if file_id in caminhos:
            return Resposta({"ok": True, "result": {"file_id": file_id, "file_path": caminhos[file_id]}})
        return Resposta({"ok": False, "description": "Bad Request: invalid file_id"})

    monkeypatch.setattr(requests, "get", falso_get)
    return pedidos, atualizacoes, caminhos


def test_tipico_respostas_primeiro_depois_diretos_sem_repetir(api):
    pedidos, atualizacoes, caminhos = api
    atualizacoes += [direto("d1"), resposta_a("r1"), {"message": {"text": "so texto"}},
                     resposta_a("d1"), direto("d2")]
    caminhos.update(r1="documents/r1.pdf", d1="documents/d1.pdf", d2="documents/d2.pdf")

    assert executar("TOKEN") == ["documents/r1.pdf", "documents/d1.pdf", "documents/d2.pdf"]
    assert pedidos == [
        URL.format("TOKEN", "getUpdates"),
        URL.format("TOKEN", "getFile?file_id=r1"),
        URL.format("TOKEN", "getFile?file_id=d1"),
        URL.format("TOKEN", "getFile?file_id=d2"),
    ]


def test_borda_sem_arquivos_e_resposta_a_mensagem_sem_documento(api):
    pedidos, atualizacoes, _ = api
    atualizacoes += [{"message": {"reply_to_message": {"text": "oi"}}}, {"edited_message": {}}]

    assert executar("T1") == []
    assert pedidos == [URL.format("T1", "getUpdates")]


def test_invalido_get_file_sem_resultado(api):
    _, atualizacoes, _ = api
    atualizacoes.append(direto("apagado"))

    with pytest.raises(KeyError):
        executar("T1")
