"""Testes da instancia LM-04: fixam o comportamento observavel de executar().

So executar() e importado. O que se fixa e o texto exato impresso (com os
codigos ANSI de cor e de cursor), as pausas pedidas a time.sleep(), as
perguntas feitas e o que a sala devolve, ou a saida por exit().

A unidade le do teclado com input() e pausa com time.sleep(); quem responde
e este arquivo, trocando os dois por dubles. A frase de abertura das salas
seguintes a primeira e sorteada entre quatro; o teste aceita qualquer uma
delas, sem prender como o sorteio e feito.
"""

import builtins
import time

import pytest

from LM_04 import executar

LIMPA_TELA, LIMPA_LINHA, LIMPA_RESTO = "\033[2J\033[0;0f", "\033[K", "\033[J"
FRASES = ["What do you want to do?", "What's next?", "Now what?", "And now?"]
RODAPE = "\nh: hint\nq: quit\n\n"
ESPERA = LIMPA_LINHA + LIMPA_RESTO


def _preparar(monkeypatch, respostas):
    """Instala os dubles; devolve (perguntas, pausas)."""
    respostas, perguntas, pausas = list(respostas), [], []

    def falso_input(pergunta=""):
        perguntas.append(pergunta)
        if not respostas:
            raise AssertionError("a unidade pediu uma entrada que o teste nao previu: %r" % pergunta)
        return respostas.pop(0)

    monkeypatch.setattr(builtins, "input", falso_input)
    monkeypatch.setattr(time, "sleep", pausas.append)
    return perguntas, pausas


def test_tipico_primeira_sala_acende_a_luz(monkeypatch, capsys):
    """Caso tipico: primeira sala, opcao 4 leva a outra sala."""
    perguntas, pausas = _preparar(monkeypatch, ["4"])

    assert executar("basement_dark", "", True) == ["basement_light", "The lights are now on."]

    assert perguntas == ["Enter your choice: "]
    assert pausas == [0.5]
    assert capsys.readouterr().out == (
        LIMPA_TELA + "\033[1;4;96mBASEMENT STORAGE ROOM\033[0m\r\n\n"
        "You're not sure how you got here. It is quite dark and there's water dripping in the distance.  \n"
        "There's a door to your left and a door to your right.  There's also a chest in the corner with a \n"
        "strange hum coming from it.\n"
        "\n"
        "What do you want to do?\r\n\n"
        "1. Open the left door\n2. Open the right door\n3. Open the chest\n"
        "4. Flick the light switch on the wall\n"
        + RODAPE + ESPERA
    )


def test_borda_dica_respostas_fora_da_faixa_acao_que_fica_e_sair(monkeypatch, capsys):
    """Borda: sala sem descricao, com mensagem anterior; 'h' mostra a dica,
    9 e 'x' sao recusados, a opcao 2 so mostra a mensagem e 'q' sai."""
    perguntas, pausas = _preparar(monkeypatch, ["h", "9", "x", "2", "q"])

    assert executar("upstairs_unlocked", "A click.", False) == ["player_quits", ""]

    assert perguntas == ["Enter your choice: "] * 5
    assert pausas == [1]
    corpo = (
        "\n"
        "{frase}\r\n\n"
        "1. Open the front door\n2. Check out the grandfather clock\n3. Open the closet\n"
        "4. Go back downstairs\n5. Play the piano\n"
        + RODAPE
        + ESPERA + "\r\n\033[0;0;32mA click by the front door?  You're almost there.  "
          "Only one thing left to do!\033[0m\n\033[3A"
        + ESPERA + "\r\n\033[1;0;91mPlease enter a number between 1 and 5.\033[0m\r\n\n\033[4A"
        + ESPERA + "\r\n\033[1;0;91m\033[0m\r\n\n\033[4A"
        + ESPERA + "\n\033[1;0;94mThe clock appears to be broken.\033[0m\n\033[3A"
        + ESPERA
    )
    cabeca = (LIMPA_TELA + "\033[1;4;96mUPSTAIRS LIVING ROOM\033[0m\r\n\n"
              "\033[0;0;33mA click.\033[0m\r\n\n")
    assert capsys.readouterr().out in [cabeca + corpo.format(frase=f) for f in FRASES]


def test_invalido_sala_inexistente_encerra_o_programa(monkeypatch, capsys):
    """Invalido: sala que nao existe mostra o erro e chama exit()."""
    perguntas, pausas = _preparar(monkeypatch, [])

    with pytest.raises(SystemExit):
        executar("sala_que_nao_existe", "", True)

    assert perguntas == [] and pausas == []
    assert capsys.readouterr().out == (
        "\r\n\033[1;0;91mProgram error: Room sala_que_nao_existe not found.  "
        "Aborting game.\033[0m\r\n\n"
    )
