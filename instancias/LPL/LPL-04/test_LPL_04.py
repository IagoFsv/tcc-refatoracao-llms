"""Testes da instancia LPL-04: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode agrupar os parametros de
simulate_quicksort, partition e quicksort num objeto, mudar as assinaturas ou
tirar as funcoes de dentro, desde que atualize as chamadas dentro da unidade;
o que nao pode mudar e o resultado, a sequencia de quadros e os ticks.

Contas do teste tipico, [1, 3, 0, 2]:
  quicksort(0, 3), partition com pivo na posicao 3 (valor 2), i = -1:
    j = 0: compara 0 e 3 (1 <= 2): i = 0, igual a j, nao troca.
    j = 1: compara 1 e 3 (3 > 2): segue.
    j = 2: compara 2 e 3 (0 <= 2): i = 1, diferente de j: troca 1 e 2,
           [1, 0, 3, 2].
    fim: i + 1 = 2, diferente de 3: troca 2 e 3, [1, 0, 2, 3]. Pivo em 2.
  quicksort(0, 1), partition com pivo na posicao 1 (valor 0), i = -1:
    j = 0: compara 0 e 1 (1 > 0): segue.
    fim: i + 1 = 0, diferente de 1: troca 0 e 1, [0, 1, 2, 3]. Pivo em 0.
  quicksort(0, -1), quicksort(1, 1) e quicksort(3, 3) nao fazem nada.
  Comparacao: 2 quadros (sem destaque, com o par). Troca: 4 quadros (sem
  destaque, com o par antes, com o par depois, sem destaque depois). Cada
  quadro e seguido de um tick. 4 comparacoes, 3 trocas e o quadro final:
  21 quadros e 21 ticks, todos com taxa 3.
"""

import pytest

from LPL_04 import executar


def _q(textos, destaque=()):
    return (tuple(textos), tuple(destaque), 40, 100)


def _compara(textos, i, j):
    return [_q(textos), _q(textos, (i, j))]


def _troca(antes, depois, i, j):
    return [_q(antes), _q(antes, (i, j)), _q(depois, (i, j)), _q(depois)]


def test_tipico_quatro_elementos_com_e_sem_troca():
    ordenado, quadros, ticks = executar([1, 3, 0, 2])

    assert ordenado == [0, 1, 2, 3]
    assert quadros == (
        _compara("1302", 0, 3)
        + _compara("1302", 1, 3)
        + _compara("1302", 2, 3)
        + _troca("1302", "1032", 1, 2)
        + _troca("1032", "1023", 2, 3)
        + _compara("1023", 0, 1)
        + _troca("1023", "0123", 0, 1)
        + [_q("0123")]
    )
    assert ticks == [3] * 21


def test_borda_lista_vazia_so_desenha_o_quadro_final():
    ordenado, quadros, ticks = executar([])

    assert ordenado == []
    assert quadros == [_q("")]
    assert ticks == [3]


def test_invalido_valores_que_nao_se_comparam():
    with pytest.raises(TypeError):
        executar([3, "a", 1])
