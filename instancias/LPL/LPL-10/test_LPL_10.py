"""Testes da instancia LPL-10: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode agrupar as coordenadas e a cor
de draw_line num objeto, mudar a assinatura ou dividir o metodo, desde que
atualize a chamada dentro da unidade; o que nao pode mudar sao os pixels
pintados na imagem devolvida, a cor padrao (preto) e o erro diante de uma
cor com numero errado de canais.

Pixels esperados: os que skimage.draw.line (scikit-image 0.26.0) devolve.
"""

import numpy as np
import pytest

from LPL_10 import executar

SEGMENTO = (0, 0, 2, 4)
PIXELS = [(0, 0), (1, 1), (1, 2), (2, 3), (2, 4)]


def _esperado(tamanho, pixels, cor):
    imagem = np.full((*tamanho, 3), 255, dtype=np.uint8)
    for linha, coluna in pixels:
        imagem[linha, coluna] = cor
    return imagem


def test_tipico_segmento_vermelho():
    imagem = executar((3, 5), SEGMENTO, (255, 0, 0))

    assert np.array_equal(imagem, _esperado((3, 5), PIXELS, (255, 0, 0)))


def test_borda_sem_cor_pinta_de_preto():
    imagem = executar((3, 5), SEGMENTO)

    assert np.array_equal(imagem, _esperado((3, 5), PIXELS, (0, 0, 0)))


def test_invalido_cor_com_dois_canais():
    with pytest.raises(ValueError):
        executar((3, 5), SEGMENTO, (255, 0))
