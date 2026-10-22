"""Testes da instancia LM-09: fixam o comportamento observavel de executar().

So executar() e importado. O que se fixa e o texto exato impresso pelos
menus, o estado final do banco card.s3db (criado na pasta atual) e a saida
por exit().

O trecho le do teclado com input() e grava num SQLite de verdade. O teste
roda numa pasta temporaria, responde o input() com um duble e troca
random.randint, usado pela classe Bank ao criar a conta, por uma sequencia
fixa, para os numeros de cartao serem conhecidos.
"""

import builtins
import random
import sqlite3

import pytest

from LM_09 import executar

# Com as sequencias de _preparar, Bank gera estes cartoes (Luhn incluso).
CARTAO_1, PIN_1 = "4000001234567899", "1234"
CARTAO_2, PIN_2 = "4000009876543219", "4321"
MENU = ["1. Create an account", "2. Log into account", "0. Exit"]
MENU_CONTA = ["1. Balance", "2. Add income", "3. Do transfer", "4. Close account",
              "5. Log out", "0. Exit"]


def _preparar(monkeypatch, tmp_path, respostas):
    monkeypatch.chdir(tmp_path)
    sorteios = [123456789, 1234, 42, 987654321, 4321, 43]
    monkeypatch.setattr(random, "randint", lambda a, b: sorteios.pop(0))
    respostas = list(respostas)

    def falso_input(pergunta=""):
        assert pergunta == "", "o trecho nao passa texto ao input()"
        if not respostas:
            raise AssertionError("a unidade pediu uma entrada que o teste nao previu")
        return respostas.pop(0)

    monkeypatch.setattr(builtins, "input", falso_input)


def _criada(cartao, pin):
    return ["Your card has been created", "Your card number:", cartao, "Your card PIN:", pin]


def _cartoes(tmp_path):
    with sqlite3.connect(tmp_path / "card.s3db") as conn:
        return conn.execute("SELECT id, number, pin, balance FROM card ORDER BY id").fetchall()


def test_tipico_cria_conta_entra_deposita_e_sai(monkeypatch, tmp_path, capsys):
    """Caso tipico: cria a conta, entra, ve o saldo, deposita 100 e sai."""
    _preparar(monkeypatch, tmp_path, ["1", "2", CARTAO_1, PIN_1, "1", "2", "100", "1", "5", "0"])

    with pytest.raises(SystemExit):
        executar()

    assert capsys.readouterr().out.splitlines() == [
        *MENU, *_criada(CARTAO_1, PIN_1),
        *MENU, "Enter your card number:", "Enter your PIN:", "You have successfully logged in!",
        *MENU_CONTA, "Balance: 0",
        *MENU_CONTA, "Enter income:", "Income was added!",
        *MENU_CONTA, "Balance: 100",
        *MENU_CONTA, "You have successfully logged out!",
        *MENU, "Bye!",
    ]
    assert _cartoes(tmp_path) == [(42, CARTAO_1, PIN_1, 100)]


def test_borda_transferencias_e_encerramento_da_conta(monkeypatch, tmp_path, capsys):
    """Borda: cartao com Luhn errado, cartao inexistente, saldo insuficiente,
    transferencia certa, encerramento da conta e login que deixa de valer."""
    _preparar(monkeypatch, tmp_path, [
        "1", "1",
        "2", CARTAO_1, PIN_1,
        "2", "50",
        "3", "4000000000000001",
        "3", "4000000000000002",
        "3", CARTAO_2, "80",
        "3", CARTAO_2, "30",
        "4",
        "2", CARTAO_1, PIN_1,
        "2", CARTAO_2, "9999",
        "0",
    ])

    with pytest.raises(SystemExit):
        executar()

    transferir = ["Transfer", "Enter card number:"]
    assert capsys.readouterr().out.splitlines() == [
        *MENU, *_criada(CARTAO_1, PIN_1),
        *MENU, *_criada(CARTAO_2, PIN_2),
        *MENU, "Enter your card number:", "Enter your PIN:", "You have successfully logged in!",
        *MENU_CONTA, "Enter income:", "Income was added!",
        *MENU_CONTA, *transferir, "Probably you made a mistake in the card number. Please try again!",
        *MENU_CONTA, *transferir, "Such a card does not exist.",
        *MENU_CONTA, *transferir, "Enter how much money you want to transfer:", "Not enough money!",
        *MENU_CONTA, *transferir, "Enter how much money you want to transfer:", "Success!",
        *MENU_CONTA, "The account has been closed!",
        *MENU, "Enter your card number:", "Enter your PIN:", "Wrong card number or PIN!",
        *MENU, "Enter your card number:", "Enter your PIN:", "Wrong card number or PIN!",
        *MENU, "Bye!",
    ]
    assert _cartoes(tmp_path) == [(43, CARTAO_2, PIN_2, 30)]


def test_invalido_opcao_do_menu_nao_numerica(monkeypatch, tmp_path, capsys):
    """Invalido: a opcao e lida com int(), entao texto levanta ValueError."""
    _preparar(monkeypatch, tmp_path, ["um"])

    with pytest.raises(ValueError):
        executar()

    assert capsys.readouterr().out.splitlines() == MENU
    assert _cartoes(tmp_path) == []
