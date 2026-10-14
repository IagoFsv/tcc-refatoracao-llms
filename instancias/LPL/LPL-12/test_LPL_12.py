"""Testes da instancia LPL-12: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode agrupar os parametros de
interpolate_df_at_fixed_x_intervals num objeto, mudar a assinatura ou
dividir a funcao, desde que atualize a chamada dentro da unidade; o que nao
pode mudar sao as colunas (nomes derivados das series de entrada e y_diff),
os valores interpolados e extrapolados e o erro diante de intervalo zero.

Contas do teste tipico: y1 = 2x nos pontos dados. y2 passa por (1.5, 3),
(2.5, 5) e (3.5, 8): inclinacao 2 no primeiro segmento e 3 no ultimo; fora
da faixa, extrapola com o segmento da ponta. Em x = 1, 2, 3, 4, 5:
y2 = 2, 4, 6.5, 9.5, 12.5 e y_diff = y1 - y2 = 0, 0, -0.5, -1.5, -2.5.
"""

import pandas as pd
import pytest

from LPL_12 import executar

DADOS1 = pd.DataFrame({"x1": [1, 2, 3, 4, 5], "y1": [2, 4, 6, 8, 10]})
DADOS2 = pd.DataFrame({"x2": [1.5, 2.5, 3.5], "y2": [3, 5, 8]})


def _esperado(xs, y1, y2):
    return pd.DataFrame({
        "x1_new": xs,
        "y1_new": y1,
        "y2_new": y2,
        "y_diff": [a - b for a, b in zip(y1, y2)],
    })


def test_tipico_intervalo_um_com_extrapolacao_nas_pontas():
    resultado = executar(DADOS1, DADOS2, 1.0)

    esperado = _esperado([1.0, 2.0, 3.0, 4.0, 5.0], [2.0, 4.0, 6.0, 8.0, 10.0],
                         [2.0, 4.0, 6.5, 9.5, 12.5])
    pd.testing.assert_frame_equal(resultado, esperado, check_dtype=False)


def test_borda_intervalo_maior_que_a_faixa_passa_do_maximo():
    # x vai de 1 ate 5 + 10 (exclusive), de 10 em 10: o segundo ponto, 11,
    # fica alem do maior x e e extrapolado.
    resultado = executar(DADOS1, DADOS2, 10)

    esperado = _esperado([1, 11], [2.0, 22.0], [2.0, 30.5])
    pd.testing.assert_frame_equal(resultado, esperado, check_dtype=False)


def test_invalido_intervalo_zero():
    # x_min e x_max sao escalares do numpy, e np.arange com passo zero levanta
    # ValueError (com numeros Python puros seria ZeroDivisionError).
    with pytest.raises(ValueError):
        executar(DADOS1, DADOS2, 0)
