"""Testes da instancia LPL-13: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode agrupar os parametros de
bilinear_interpolation em objetos (ponto, retangulo, valores), mudar a
assinatura ou dividir a funcao, desde que atualize a chamada dentro da
unidade; o que nao pode mudar e o valor interpolado e o erro diante de um
retangulo degenerado.

Conta do teste tipico: ponto (1.5, 3) no retangulo x de 1 a 3, y de 2 a 6,
valores z11=1, z12=2, z21=3, z22=5. O retangulo nao comeca em zero, para
que x - x1 e x + x1 deem resultados diferentes.
  1*1.5*3 + 3*0.5*3 + 2*1.5*1 + 5*0.5*1 = 4.5 + 4.5 + 3 + 2.5 = 14.5
  14.5 / (2*4) = 1.8125
"""

import pytest

from LPL_13 import executar

CANTOS = (1, 3, 2, 6)
VALORES = (1, 2, 3, 5)


def test_tipico_ponto_assimetrico_dentro_do_retangulo():
    assert executar((1.5, 3), CANTOS, VALORES) == pytest.approx(1.8125)


def test_borda_ponto_no_canto_devolve_o_valor_do_canto():
    # (x2, y2) e o canto de z22; (x2, y1) e o de z21.
    assert executar((3, 6), CANTOS, VALORES) == pytest.approx(5)
    assert executar((3, 2), CANTOS, VALORES) == pytest.approx(3)


def test_invalido_retangulo_sem_largura():
    with pytest.raises(ZeroDivisionError):
        executar((2, 3), (2, 2, 2, 6), VALORES)
