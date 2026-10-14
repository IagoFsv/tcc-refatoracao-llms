"""Testes da instancia LPL-11: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode agrupar o centro, o raio e a
cor de draw_circle num objeto, mudar a assinatura ou dividir o metodo,
desde que atualize a chamada dentro da unidade; o que nao pode mudar sao os
pixels pintados na imagem devolvida, a cor padrao (preto), o recorte na
borda e o erro diante de uma cor com numero errado de canais.

O centro e dado como (x, y): x e a coluna, y e a linha. Pixels esperados:
os que skimage.draw.disk (scikit-image 0.26.0) devolve; com raio 2, o disco
e o quadrado 3x3 em volta do centro.
"""

import numpy as np
import pytest

from LPL_11 import executar


def _esperado(tamanho, pixels, cor):
    imagem = np.full((*tamanho, 3), 255, dtype=np.uint8)
    for linha, coluna in pixels:
        imagem[linha, coluna] = cor
    return imagem


def test_tipico_disco_azul_no_meio():
    imagem = executar((7, 7), (4, 2, 2), (0, 0, 255))

    pixels = [(l, c) for l in (1, 2, 3) for c in (3, 4, 5)]
    assert np.array_equal(imagem, _esperado((7, 7), pixels, (0, 0, 255)))


def test_borda_disco_recortado_no_canto_sem_cor_pinta_de_preto():
    imagem = executar((4, 5), (1, 0, 2))

    pixels = [(l, c) for l in (0, 1) for c in (0, 1, 2)]
    assert np.array_equal(imagem, _esperado((4, 5), pixels, (0, 0, 0)))


def test_invalido_cor_com_dois_canais():
    with pytest.raises(ValueError):
        executar((7, 7), (4, 2, 2), (0, 255))
