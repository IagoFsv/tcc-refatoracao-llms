"""Testes da instancia MNC-19: fixam o comportamento observavel de executar().

So executar() e importado. O mapa tem 2 x 3 x 4 casas. A refatoracao pode
reorganizar o acesso ao mapa; o que nao pode mudar e a casa devolvida
(indices negativos contando do fim, como em listas Python) e o erro diante
de posicao fora do mapa.
"""

import pytest

from MNC_19 import executar


def test_tipico_casa_da_posicao_pedida():
    assert executar(1, 2, 3) == (1, 2, 3)
    assert executar(0, 1, 2) == (0, 1, 2)


def test_borda_origem_e_indices_negativos():
    assert executar(0, 0, 0) == (0, 0, 0)
    assert executar(-1, -1, -1) == (1, 2, 3)
    assert executar(-2, 0, -4) == (0, 0, 0)


def test_invalido_posicao_fora_do_mapa():
    with pytest.raises(IndexError):
        executar(0, 0, 4)
