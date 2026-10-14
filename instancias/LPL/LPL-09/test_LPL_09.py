"""Testes da instancia LPL-09: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode agrupar as coordenadas de
draw_line num objeto, mudar a assinatura ou dividir o metodo, desde que
atualize a chamada dentro da unidade; o que nao pode mudar sao os pixels
marcados na imagem devolvida e o erro diante de ponto fora da imagem.

Pixels esperados: os que skimage.draw.line (scikit-image 0.26.0) devolve.
"""

import numpy as np
import pytest

from LPL_09 import executar


def _esperado(tamanho, pixels):
    imagem = np.zeros(tamanho)
    for linha, coluna in pixels:
        imagem[linha, coluna] = 1
    return imagem


def test_tipico_segmento_inclinado():
    imagem = executar((3, 5), (0, 0, 2, 4))

    pixels = [(0, 0), (1, 1), (1, 2), (2, 3), (2, 4)]
    assert np.array_equal(imagem, _esperado((3, 5), pixels))


def test_borda_segmento_de_um_ponto_so():
    imagem = executar((5, 5), (2, 3, 2, 3))

    assert np.array_equal(imagem, _esperado((5, 5), [(2, 3)]))


def test_invalido_ponto_fora_da_imagem():
    with pytest.raises(IndexError):
        executar((5, 5), (0, 0, 0, 9))
