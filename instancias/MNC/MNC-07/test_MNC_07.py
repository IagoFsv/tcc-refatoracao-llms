"""Testes da instancia MNC-07: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode dar nome as matrizes e aos
indices; o que nao pode mudar e a pontuacao devolvida para cada tabuleiro
(pesos por tamanho de sequencia, sequencias bloqueadas pelo adversario ou
por bloqueio nao contam, +inf/-inf quando alguem ja venceu) e o erro diante
de jogador inexistente.

Os valores esperados vem da execucao do codigo original.
"""

import pytest

from MNC_07 import executar


def test_tipico_pontuacao_simetrica_para_os_dois_jogadores():
    tabuleiro = ["XX..",
                 ".O..",
                 "..X.",
                 "O..."]

    assert executar(tabuleiro, 3, "X") == 20
    assert executar(tabuleiro, 3, "O") == -20
    assert executar(tabuleiro, 4, "X") == 12

    em_coluna = ["X...",
                 "X...",
                 "....",
                 "O..."]
    assert executar(em_coluna, 3, "X") == 24


def test_borda_tabuleiro_vazio_vitoria_e_bloqueio():
    assert executar(["....", "....", "....", "...."], 3, "X") == 0

    vitoria_de_x = ["XXX.",
                    ".O..",
                    "O...",
                    "...."]
    assert executar(vitoria_de_x, 3, "X") == float("inf")
    assert executar(vitoria_de_x, 3, "O") == float("-inf")

    com_bloqueio = ["X.*..",
                    ".X...",
                    "..O..",
                    "...O.",
                    "....."]
    assert executar(com_bloqueio, 3, "X") == -48
    assert executar(com_bloqueio, 4, "X") == -16

    adversario_e_bloqueio_na_mesma_linha = ["XO*.",
                                            "....",
                                            "OX*.",
                                            "X..."]
    assert executar(adversario_e_bloqueio_na_mesma_linha, 3, "X") == 28
    assert executar(adversario_e_bloqueio_na_mesma_linha, 3, "O") == -28


def test_invalido_jogador_inexistente():
    with pytest.raises(KeyError):
        executar(["X..", "...", "..."], 3, "Z")
