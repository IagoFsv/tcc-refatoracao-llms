"""Testes da instancia LM-11: fixam o comportamento observavel de executar().

So executar() e importado. O que se fixa e o texto exato impresso para cada
numero de erros (8 linhas por desenho) e que nada e impresso fora de 0 a 6.
"""

from LM_11 import executar

TOPO = ["_________", "|       |"]
VAZIA = "|"


def _saida(capsys):
    return capsys.readouterr().out.splitlines()


def test_tipico_tres_erros_cabeca_e_braco(capsys):
    """Caso tipico: com 3 erros aparecem cabeca, tronco e um braco."""
    executar(3)
    assert _saida(capsys) == TOPO + ["|       O", "|      /|"] + [VAZIA] * 4


def test_borda_todos_os_desenhos_de_0_a_6(capsys):
    """Borda: os extremos (0 e 6) e cada passo intermediario."""
    corpo = [
        [],
        ["|       O"],
        ["|       O", "|       |"],
        ["|       O", "|      /|"],
        ["|       O", "|      /|\\"],
        ["|       O", "|      /|\\", "|      /"],
        ["|       O", "|      /|\\", "|      / \\"],
    ]
    for erros, partes in enumerate(corpo):
        executar(erros)
        assert _saida(capsys) == TOPO + partes + [VAZIA] * (6 - len(partes)), erros


def test_invalido_fora_de_0_a_6_nao_imprime_nada(capsys):
    """Invalido: 7, negativo ou texto nao casam com nenhum caso e nao ha erro."""
    for erros in (7, -1, "3"):
        assert executar(erros) is None
        assert capsys.readouterr().out == "", erros
