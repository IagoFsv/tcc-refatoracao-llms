"""Testes da instancia LPL-02: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode agrupar os parametros de train
num objeto, mudar a assinatura ou dividir a funcao, desde que atualize a
chamada dentro da unidade; o que nao pode mudar e a perda, a acuracia, o
estado final do modelo e o erro diante de dataset vazio.

Contas do teste tipico (3 classes, vies inicial zero, taxa 0.5):
  lote 1: acerta a 1a amostra, erra a 2a (preve 1, era 2). Perda media 0.5.
          Gradiente [0, 0.5, -0.5], vies vira [0, -0.25, 0.25].
  lote 2: com o vies novo acerta a 1a amostra (sem o passo do lote 1, o
          empate entre as classes 1 e 2 daria a classe 1, errada) e erra a
          2a (preve 2, era 0). Perda media 0.625. Gradiente [-0.5, 0, 0.5]
          (so do lote 2: o gradiente e zerado entre os lotes), vies vira
          [0.25, -0.25, 0].
  perda: (0.5 + 0.625) / 4 amostras = 0.28125. O original soma as medias
  dos lotes e divide pelo numero de amostras; fixado como e.
  acuracia: 2 acertos em 4 = 50.0.
"""

import pytest

from LPL_02 import executar


def test_tipico_dois_lotes_com_acertos_e_erros():
    lotes = [
        ([[3, 1, 0], [0, 2, 1]], [0, 2]),
        ([[1, 2, 2], [0, 0, 1]], [2, 0]),
    ]

    perda, acuracia, vies, em_treino = executar(lotes)

    assert perda == pytest.approx(0.28125)
    assert acuracia == pytest.approx(50.0)
    assert vies == pytest.approx([0.25, -0.25, 0.0])
    assert em_treino is True


def test_borda_um_lote_todo_certo_nao_mexe_no_modelo():
    perda, acuracia, vies, em_treino = executar([([[5, 1, 0], [0, 0, 4]], [0, 2])])

    assert perda == pytest.approx(0.0)
    assert acuracia == pytest.approx(100.0)
    assert vies == pytest.approx([0.0, 0.0, 0.0])
    assert em_treino is True


def test_invalido_dataset_vazio():
    with pytest.raises(ZeroDivisionError):
        executar([])
