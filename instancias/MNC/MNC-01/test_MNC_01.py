"""Testes da instancia MNC-01: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode trocar os acessos encadeados
por funcoes auxiliares, variaveis intermediarias ou classes; o que nao pode
mudar e o dicionario devolvido, o JSON impresso e o erro diante de dado
faltando.

O catalogo de ranks (dois ranks, tres objetivos) e fixo e vive na unidade.
Aqui muda so a resposta da API, montada por _rec e _resposta.
"""

import json

import pytest

from MNC_01 import executar


def _rec(completo, total, progresso):
    """Um registro da API com um unico objetivo."""
    return {"objectives": [
        {"complete": completo, "completionValue": total, "progress": progresso}
    ]}


def _resposta(personagens, registros_personagem, registros_perfil,
              variaveis_perfil, variaveis_personagem):
    """Monta a resposta da API no formato que a unidade consome."""
    return {
        "characters": {"data": personagens},
        "characterRecords": {"data": {
            cid: {"records": regs} for cid, regs in registros_personagem.items()
        }},
        "profileRecords": {"data": {"records": registros_perfil}},
        "profileStringVariables": {"data": {"integerValuesByHash": variaveis_perfil}},
        "characterStringVariables": {"data": {
            cid: {"integerValuesByHash": v} for cid, v in variaveis_personagem.items()
        }},
    }


def _dados_tipicos():
    """Dois personagens; o jogado por ultimo (2) vem depois no dicionario."""
    return _resposta(
        personagens={
            "a": {"characterId": 1, "dateLastPlayed": "2024-01-10T12:00:00"},
            "b": {"characterId": 2, "dateLastPlayed": "2024-03-05T08:00:00"},
        },
        registros_personagem={
            # O personagem 1 tem tudo diferente: se a unidade escolher o
            # personagem errado, o resultado muda.
            "1": {"9001": _rec(False, 1, 0), "1001": _rec(False, 10, 2),
                  "1002": _rec(False, 500, 7)},
            "2": {"9001": _rec(True, 1, 1), "1001": _rec(True, 10, 10),
                  "1002": _rec(False, 500, 120)},
        },
        registros_perfil={"9002": _rec(False, 1, 0), "1003": _rec(False, 3, 1)},
        variaveis_perfil={"111": 120},
        variaveis_personagem={"1": {"222": 99}, "2": {"222": 3}},
    )


def test_tipico_escolhe_o_ultimo_personagem_e_monta_os_ranks(capsys):
    resultado = executar(_dados_tipicos())

    assert resultado == {
        "9001": {
            "completed": True,
            "record_sets": {
                "501": {
                    "completed": False,
                    "records": {
                        "1001": {"completed": True, "completionValue": 10, "progress": 10},
                        "1002": {"completed": False, "completionValue": 500,
                                 "progress": 120, "variables": {"111": 120}},
                    },
                },
            },
        },
        "9002": {
            "completed": False,
            "record_sets": {
                "502": {
                    "completed": False,
                    "records": {
                        "1003": {"completed": False, "completionValue": 3,
                                 "progress": 1, "variables": {"111": 120, "222": 3}},
                    },
                },
            },
        },
    }
    assert capsys.readouterr().out == json.dumps(resultado, indent=2) + "\n"


def test_borda_um_so_personagem_com_tudo_completo(capsys):
    dados = _resposta(
        personagens={"x": {"characterId": 7, "dateLastPlayed": "2024-01-01T00:00:00"}},
        registros_personagem={
            "7": {"9001": _rec(True, 1, 1), "1001": _rec(True, 10, 10),
                  "1002": _rec(True, 500, 500)},
        },
        registros_perfil={"9002": _rec(True, 1, 1), "1003": _rec(True, 3, 3)},
        variaveis_perfil={"111": 500},
        variaveis_personagem={"7": {"222": 3}},
    )

    resultado = executar(dados)

    assert [r["completed"] for r in resultado.values()] == [True, True]
    assert resultado["9001"]["record_sets"]["501"]["completed"] is True
    assert resultado["9002"]["record_sets"]["502"]["completed"] is True
    assert resultado["9002"]["record_sets"]["502"]["records"]["1003"]["variables"] == {
        "111": 500, "222": 3,
    }
    assert capsys.readouterr().out == json.dumps(resultado, indent=2) + "\n"


def test_invalido_registro_de_objetivo_ausente():
    dados = _dados_tipicos()
    del dados["characterRecords"]["data"]["2"]["records"]["1002"]

    with pytest.raises(KeyError):
        executar(dados)
