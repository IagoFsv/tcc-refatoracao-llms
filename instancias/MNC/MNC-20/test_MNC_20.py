"""Testes da instancia MNC-20: fixam o comportamento observavel de executar().

So executar() e importado. executar recebe as descricoes do mapa como
descricoes[x][y][z]. A refatoracao pode reorganizar a montagem da cena e os
lacos; o que nao pode mudar e o texto impresso (100 linhas em branco para
limpar a tela, uma linha por (x, y) com as descricoes de z coladas, e uma
linha em branco no fim) e o erro diante de mapa irregular.
"""

import pytest

from MNC_20 import executar

LIMPA_TELA = "\n" * 101  # print("\n" * 100) mais a quebra do proprio print


def test_tipico_uma_linha_por_x_e_y(capsys):
    executar([[["a", "b"], ["c", "d"]],
              [["e", "f"], ["g", "h"]]])

    assert capsys.readouterr().out == LIMPA_TELA + "ab\ncd\nef\ngh\n" + "\n"


def test_borda_descricoes_vazias_e_mapa_de_uma_casa(capsys):
    executar([[["", "~"], ["#", ""]]])
    assert capsys.readouterr().out == LIMPA_TELA + "~\n#\n" + "\n"

    executar([[["@"]]])
    assert capsys.readouterr().out == LIMPA_TELA + "@\n" + "\n"


def test_invalido_mapa_irregular():
    with pytest.raises(IndexError):
        executar([[["a", "b"], ["c"]]])
