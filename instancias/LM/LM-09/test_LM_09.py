"""Tests for instance LM-09: they pin the observable behavior of run().

Only run() is imported. What is pinned is the exact text printed by the
menus, the final state of the card.s3db database (created in the current
folder) and the exit through exit().

The code reads from the keyboard with input() and writes to a real SQLite.
The test runs in a temporary folder, answers input() with a double and
replaces random.randint, used by the Bank class when creating the account,
with a fixed sequence, so the card numbers are known.
"""

import builtins
import random
import sqlite3

import pytest

from LM_09 import run

# With the sequences in _prepare, Bank generates these cards (Luhn included).
CARD_1, PIN_1 = "4000001234567899", "1234"
CARD_2, PIN_2 = "4000009876543219", "4321"
MENU = ["1. Create an account", "2. Log into account", "0. Exit"]
ACCOUNT_MENU = ["1. Balance", "2. Add income", "3. Do transfer", "4. Close account",
                "5. Log out", "0. Exit"]


def _prepare(monkeypatch, tmp_path, answers):
    monkeypatch.chdir(tmp_path)
    draws = [123456789, 1234, 42, 987654321, 4321, 43]
    monkeypatch.setattr(random, "randint", lambda a, b: draws.pop(0))
    answers = list(answers)

    def fake_input(prompt=""):
        assert prompt == "", "the code does not pass text to input()"
        if not answers:
            raise AssertionError("the unit asked for an input the test did not expect")
        return answers.pop(0)

    monkeypatch.setattr(builtins, "input", fake_input)


def _created(card, pin):
    return ["Your card has been created", "Your card number:", card, "Your card PIN:", pin]


def _cards(tmp_path):
    with sqlite3.connect(tmp_path / "card.s3db") as conn:
        return conn.execute("SELECT id, number, pin, balance FROM card ORDER BY id").fetchall()


def test_typical_creates_account_logs_in_deposits_and_exits(monkeypatch, tmp_path, capsys):
    """Typical case: creates the account, logs in, checks the balance, deposits 100 and exits."""
    _prepare(monkeypatch, tmp_path, ["1", "2", CARD_1, PIN_1, "1", "2", "100", "1", "5", "0"])

    with pytest.raises(SystemExit):
        run()

    assert capsys.readouterr().out.splitlines() == [
        *MENU, *_created(CARD_1, PIN_1),
        *MENU, "Enter your card number:", "Enter your PIN:", "You have successfully logged in!",
        *ACCOUNT_MENU, "Balance: 0",
        *ACCOUNT_MENU, "Enter income:", "Income was added!",
        *ACCOUNT_MENU, "Balance: 100",
        *ACCOUNT_MENU, "You have successfully logged out!",
        *MENU, "Bye!",
    ]
    assert _cards(tmp_path) == [(42, CARD_1, PIN_1, 100)]


def test_edge_transfers_and_closing_the_account(monkeypatch, tmp_path, capsys):
    """Edge: card with a wrong Luhn digit, nonexistent card, insufficient
    balance, valid transfer, closing the account and a login that stops working."""
    _prepare(monkeypatch, tmp_path, [
        "1", "1",
        "2", CARD_1, PIN_1,
        "2", "50",
        "3", "4000000000000001",
        "3", "4000000000000002",
        "3", CARD_2, "80",
        "3", CARD_2, "30",
        "4",
        "2", CARD_1, PIN_1,
        "2", CARD_2, "9999",
        "0",
    ])

    with pytest.raises(SystemExit):
        run()

    transfer = ["Transfer", "Enter card number:"]
    assert capsys.readouterr().out.splitlines() == [
        *MENU, *_created(CARD_1, PIN_1),
        *MENU, *_created(CARD_2, PIN_2),
        *MENU, "Enter your card number:", "Enter your PIN:", "You have successfully logged in!",
        *ACCOUNT_MENU, "Enter income:", "Income was added!",
        *ACCOUNT_MENU, *transfer, "Probably you made a mistake in the card number. Please try again!",
        *ACCOUNT_MENU, *transfer, "Such a card does not exist.",
        *ACCOUNT_MENU, *transfer, "Enter how much money you want to transfer:", "Not enough money!",
        *ACCOUNT_MENU, *transfer, "Enter how much money you want to transfer:", "Success!",
        *ACCOUNT_MENU, "The account has been closed!",
        *MENU, "Enter your card number:", "Enter your PIN:", "Wrong card number or PIN!",
        *MENU, "Enter your card number:", "Enter your PIN:", "Wrong card number or PIN!",
        *MENU, "Bye!",
    ]
    assert _cards(tmp_path) == [(43, CARD_2, PIN_2, 30)]


def test_invalid_non_numeric_menu_option(monkeypatch, tmp_path, capsys):
    """Invalid: the option is read with int(), so text raises ValueError."""
    _prepare(monkeypatch, tmp_path, ["one"])

    with pytest.raises(ValueError):
        run()

    assert capsys.readouterr().out.splitlines() == MENU
    assert _cards(tmp_path) == []
