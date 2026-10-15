"""Testes da instancia MNC-13: fixam o comportamento observavel de executar().

So executar() e importado. O teste roda numa pasta temporaria (onde users.log
e gravado), intercepta requests.get com respostas gravadas da API de bots e
fixa o relogio trocando datetime.datetime. A refatoracao pode reorganizar o
acesso ao JSON; o que nao pode mudar e a URL pedida, o valor devolvido para
cada endpoint, as linhas acrescentadas ao users.log e os erros.

Os testes fixam o comportamento como ele e: no users.log o id vem antes do
nome de usuario (as variaveis do laco estao trocadas no original).
"""

import datetime

import pytest
import requests

from MNC_13 import executar


class Resposta:
    def __init__(self, dados, status_code=200, text="{}"):
        self.dados = dados
        self.status_code = status_code
        self.text = text

    def json(self):
        return self.dados


class RelogioFixo(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 10, 14, 9, 30, 0)


@pytest.fixture
def api(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(datetime, "datetime", RelogioFixo)
    pedidos = []
    respostas = {}

    def falso_get(url, *args, **kwargs):
        pedidos.append(url)
        return respostas["resposta"]

    monkeypatch.setattr(requests, "get", falso_get)
    return tmp_path, pedidos, respostas


def atualizacao(user_id, username=None):
    remetente = {"id": user_id}
    if username is not None:
        remetente["username"] = username
    return {"message": {"from": remetente, "text": "oi"}}


def test_tipico_get_updates_lista_usuarios_sem_repetir_e_grava_log(api):
    pasta, pedidos, respostas = api
    resultado = [atualizacao(11, "ana"), atualizacao(22, "bia"), atualizacao(11, "ana"),
                 atualizacao(33), {"edited_message": {}}]
    respostas["resposta"] = Resposta({"ok": True, "result": resultado})

    assert executar("TOKEN", "getUpdates") == [(11, "ana"), (22, "bia")]
    assert pedidos == ["https://api.telegram.org/botTOKEN/getUpdates"]
    assert (pasta / "users.log").read_text() == (
        "2026-10-14 09:30:00, TOKEN, 11, ana\n"
        "2026-10-14 09:30:00, TOKEN, 22, bia\n"
    )


def test_borda_get_me_outro_endpoint_e_log_acumulado(api):
    pasta, pedidos, respostas = api
    perfil = {"id": 99, "is_bot": True, "first_name": "Robo", "username": "robo_bot"}
    respostas["resposta"] = Resposta({"ok": True, "result": perfil})
    assert executar("T1", "getMe") == ("robo_bot", "Robo", 99)

    respostas["resposta"] = Resposta({"ok": True, "result": True})
    assert executar("T1", "deleteWebhook") is None

    (pasta / "users.log").write_text("linha antiga\n")
    respostas["resposta"] = Resposta({"ok": True, "result": [atualizacao(5, "caio")]})
    executar("T1", "getUpdates")
    assert (pasta / "users.log").read_text() == "linha antiga\n2026-10-14 09:30:00, T1, 5, caio\n"
    assert pedidos == [
        "https://api.telegram.org/botT1/getMe",
        "https://api.telegram.org/botT1/deleteWebhook",
        "https://api.telegram.org/botT1/getUpdates",
    ]


def test_invalido_status_de_erro_e_perfil_incompleto(api):
    _, _, respostas = api
    respostas["resposta"] = Resposta({}, status_code=401, text='{"ok":false,"error_code":401}')
    with pytest.raises(Exception, match=r'^Error: \{"ok":false,"error_code":401\}$'):
        executar("RUIM", "getUpdates")

    respostas["resposta"] = Resposta({"ok": True, "result": {"id": 1}}, text="sem nome")
    with pytest.raises(Exception, match="^Error: sem nome$"):
        executar("T1", "getMe")
