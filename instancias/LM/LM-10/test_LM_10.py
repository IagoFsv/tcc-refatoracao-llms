"""Testes da instancia LM-10: fixam o comportamento observavel de executar().

So executar() e importado. O que se fixa e o que a calculadora pergunta, na
ordem em que pergunta, e o texto exato que ela imprime, inclusive quando o
usuario pede para calcular de novo.

A unidade le do teclado com input(); quem responde e este arquivo, trocando
input() por um duble com as respostas na ordem.
"""

import builtins

import pytest

from LM_10 import executar

MENU = ("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n"
        " 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n"
        " 6 for calories needed to maintain weight \n"
        " 7. for calculating everything from bmi and activity level\n Enter your choice: ")
ATIVIDADE = ("What is your activity level? Sedentary = 1.2, lightly active = 1.375, "
             "moderately active = 1.55, very active = 1.725, extra active = 1.9")
DE_NOVO = "Do you want to calculate again? y/n: "
TRACO = "-" * 40
PESO, ALTURA_CM, IDADE = "What is your weight in kg?", "What is your height in cm?", "What is your age in years?"


def _teclado(monkeypatch, respostas):
    """Instala o duble de input() e devolve a lista das perguntas feitas."""
    respostas, perguntas = list(respostas), []

    def falso_input(pergunta=""):
        perguntas.append(pergunta)
        if not respostas:
            raise AssertionError("a unidade pediu uma entrada que o teste nao previu: %r" % pergunta)
        return respostas.pop(0)

    monkeypatch.setattr(builtins, "input", falso_input)
    return perguntas


def test_tipico_opcao_7_calcula_tudo(monkeypatch, capsys):
    """Caso tipico: opcao 7 com 70 kg, 175 cm, 30 anos e atividade 2."""
    perguntas = _teclado(monkeypatch, ["7", "70", "175", "30", "2", "n"])

    executar()

    assert perguntas == [MENU, "what is your weight in kg?", "what is your height in cm?",
                         "what is your age in years?", ATIVIDADE, DE_NOVO]
    assert capsys.readouterr().out.splitlines() == [
        "Your BMI is 22.857142857142858",
        "Your bmr is 1643.75",
        "Your tdee is 3287.5",
        "You need 2787.5 calories to lose weight",
        "You need 3787.5 calories to gain weight",
        "You need 3287.5 calories to maintain weight",
        TRACO,
        "Goodbye, See You on The Other Side!",
        TRACO,
    ]


def test_borda_calcular_de_novo_percorre_as_opcoes_e_termina_em_opcao_invalida(monkeypatch, capsys):
    """Borda: 'y' reinicia o menu; passa por 1, 2, 4, 5 e 6 e para na opcao 9."""
    medidas = ["70", "175", "30"]
    perguntas = _teclado(monkeypatch, ["1", "70", "2", "y",
                                       "2", *medidas, "y",
                                       "4", *medidas, "2", "y",
                                       "5", *medidas, "2", "y",
                                       "6", *medidas, "2", "y",
                                       "9"])

    executar()

    de_novo = [TRACO, "Sure, let's do it again", TRACO]
    assert capsys.readouterr().out.splitlines() == [
        "Your BMI is 17.5", *de_novo,
        "Your bmr is 1643.75", *de_novo,
        "You need 2787.5 calories to lose weight", *de_novo,
        "You need 3787.5 calories to gain weight", *de_novo,
        "You need 3287.5 calories to maintain weight", *de_novo,
        "Invalid number, choose a wise one next time",
    ]
    tres = [PESO, ALTURA_CM, IDADE]
    assert perguntas == [MENU, PESO, "What is your height in meters?", DE_NOVO,
                         MENU, *tres, DE_NOVO,
                         MENU, *tres, ATIVIDADE, DE_NOVO,
                         MENU, *tres, ATIVIDADE, DE_NOVO,
                         MENU, *tres, ATIVIDADE, DE_NOVO,
                         MENU]


def test_invalido_nivel_de_atividade_decimal(monkeypatch, capsys):
    """Invalido: a pergunta sugere 1.2, mas a resposta e lida com int()."""
    perguntas = _teclado(monkeypatch, ["3", "70", "175", "30", "1.2"])

    with pytest.raises(ValueError):
        executar()

    assert perguntas == [MENU, PESO, ALTURA_CM, IDADE, ATIVIDADE]
    assert capsys.readouterr().out == ""
