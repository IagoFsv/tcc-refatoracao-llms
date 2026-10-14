"""Testes da instancia LPL-03: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode agrupar os parametros de
simulate_heapsort e de heapify num objeto, mudar as assinaturas ou tirar
heapify de dentro, desde que atualize as chamadas dentro da unidade; o que
nao pode mudar e o resultado, a sequencia de quadros da animacao e os ticks.

Contas do teste tipico, [2, 3, 1] (n = 3):
  montagem do heap, i de 3 a 0: so i = 0 tem filhos.
    compara 0 e 1 (2 <= 3, o maior vira 1), compara 1 e 2 (3 > 1, fica 1),
    compara 0 e 1 de novo antes de trocar; troca: [3, 2, 1].
  extracao, i = 2: troca 2 e 0: [1, 2, 3]. heapify(n=2, 0): compara 0 e 1
    (1 <= 2), compara 0 e 1 de novo, troca: [2, 1, 3].
  extracao, i = 1: troca 1 e 0: [1, 2, 3]. heapify(n=1, 0) nao compara.
  Cada comparacao desenha 2 quadros (sem destaque, depois com o par
  destacado), com um tick depois de cada; no fim, 1 quadro e 1 tick.
  5 comparacoes: 11 quadros e 11 ticks, todos com taxa 3.
"""

import pytest

from LPL_03 import executar


def _q(textos, destaque=()):
    return (tuple(textos), tuple(destaque), 40, 100)


def test_tipico_tres_elementos_fora_de_ordem():
    ordenado, quadros, ticks = executar([2, 3, 1])

    assert ordenado == [1, 2, 3]
    assert quadros == [
        _q("231"), _q("231", (0, 1)),
        _q("231"), _q("231", (1, 2)),
        _q("231"), _q("231", (0, 1)),
        _q("123"), _q("123", (0, 1)),
        _q("123"), _q("123", (0, 1)),
        _q("123"),
    ]
    assert ticks == [3] * 11


def test_borda_lista_vazia_so_desenha_o_quadro_final():
    ordenado, quadros, ticks = executar([])

    assert ordenado == []
    assert quadros == [_q("")]
    assert ticks == [3]


def test_invalido_valores_que_nao_se_comparam():
    with pytest.raises(TypeError):
        executar([3, "a", 1])
