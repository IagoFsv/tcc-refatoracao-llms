"""Testes da instancia LM-03: fixam o comportamento observavel de executar().

So executar() e importado. A funcao e pura: o que se fixa e o par
(colunas, linhas) devolvido para cada numero de elementos, inclusive nos
limites entre faixas, e o erro para o que nao cai em faixa nenhuma.
"""

import pytest

from LM_03 import executar


# (primeiro, ultimo, resultado) de cada faixa da tabela, de 1 a 91.
FAIXAS = [
    (1, 1, (1, 1)), (2, 2, (2, 1)), (3, 3, (3, 1)), (4, 4, (4, 1)), (5, 5, (5, 1)),
    (6, 6, (6, 1)), (7, 8, (4, 2)), (9, 10, (5, 2)), (11, 12, (6, 2)),
    (13, 18, (6, 3)), (19, 24, (6, 4)), (25, 30, (6, 5)), (31, 35, (7, 5)),
    (36, 42, (7, 6)), (43, 49, (7, 7)), (50, 56, (7, 8)), (57, 63, (7, 9)),
    (64, 70, (7, 10)), (71, 77, (7, 11)), (78, 84, (7, 12)), (85, 91, (7, 13)),
]


def test_tipico_toda_a_tabela_de_1_a_91():
    """Caso tipico: cada inteiro de 1 a 91 cai na sua faixa da tabela."""
    for primeiro, ultimo, resultado in FAIXAS:
        for elementos in range(primeiro, ultimo + 1):
            assert executar(elementos) == resultado, elementos


def test_borda_limites_das_faixas_e_proporcao_aurea():
    """Borda: zero e negativos, viradas de faixa e o calculo acima de 91."""
    assert executar(-3) == (1, 1)
    assert executar(0) == (1, 1)
    assert executar(1) == (1, 1)
    assert executar(6) == (6, 1)
    assert executar(12) == (6, 2)
    assert executar(13) == (6, 3)
    assert executar(18) == (6, 3)
    assert executar(35) == (7, 5)
    assert executar(36) == (7, 6)
    assert executar(91) == (7, 13)
    assert executar(92) == (7, 14)
    assert executar(100) == (7, 15)
    assert executar(1000) == (24, 42)


def test_invalido_numero_fracionario_fora_das_faixas():
    """Invalido: 12.5 nao e igual a nenhum inteiro nem cai em range()."""
    with pytest.raises(ValueError, match="Unsupported number of elements: 12.5"):
        executar(12.5)
