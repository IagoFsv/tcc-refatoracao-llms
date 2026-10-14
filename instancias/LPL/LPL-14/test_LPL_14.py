"""Testes da instancia LPL-14: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode agrupar os parametros de
simulate_bouncing_ball em objetos (estado inicial, tempo, fisica), mudar a
assinatura ou dividir a funcao, desde que atualize a chamada dentro da
unidade; o que nao pode mudar sao as posicoes devolvidas, os valores padrao
de restituicao (0.2) e gravidade (9.83) e o erro diante de numero de passos
nao inteiro.

Peculiaridade do original, fixada como e: quando a bola nao passa do chao,
a posicao y recebe vy * dt duas vezes no mesmo passo, e o y guardado pode
ficar negativo (o quique so acontece no passo seguinte).

Contas do teste tipico (x0=0, y0=0.3, vx=1, vy=-2, dt=0.1, restituicao 0.5,
g=10):
  passo 1: y = 0.3 - 0.2 = 0.1 (nao negativo) -> y = 0.1 - 0.2 = -0.1;
           vy = -2 - 1 = -3
  passo 2: y = -0.1 - 0.3 = -0.4 (negativo) -> quica: vy = 1.5, y = 0
  passo 3: y = 0 + 0.15 = 0.15 -> y = 0.15 + 0.15 = 0.3; vy = 0.5

Contas do teste de borda (parada no chao, valores padrao, dt=0.1):
  passo 1: y = 0 (nao negativo) -> y = 0; vy = -0.983
  passo 2: y = -0.0983 (negativo) -> quica: vy = 0.983 * 0.2 = 0.1966, y = 0
  passo 3: y = 0.01966 -> y = 0.03932
"""

import pytest

from LPL_14 import executar


def test_tipico_bola_desce_fica_abaixo_do_chao_e_quica():
    xs, ys = executar((0, 0.3, 1, -2), (3, 0.1), (0.5, 10))

    assert xs == pytest.approx([0, 0.1, 0.2, 0.3])
    assert ys == pytest.approx([0.3, -0.1, 0, 0.3])


def test_borda_parada_no_chao_com_valores_padrao():
    xs, ys = executar((0, 0, 0, 0), (3, 0.1))

    assert xs == pytest.approx([0, 0, 0, 0])
    assert ys == pytest.approx([0, 0, 0, 0.03932])

    xs, ys = executar((2, 5, 1, 1), (0, 0.1))  # zero passos: so a posicao inicial

    assert xs == [2]
    assert ys == [5]


def test_invalido_numero_de_passos_nao_inteiro():
    with pytest.raises(TypeError):
        executar((0, 1, 1, 0), (2.5, 0.1))
