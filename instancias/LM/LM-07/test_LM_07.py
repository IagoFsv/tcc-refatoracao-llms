"""Testes da instancia LM-07: fixam o comportamento observavel de executar().

So executar() e importado. O que se fixa e o que o gerador pergunta, na
ordem em que pergunta, o texto que imprime, o arquivo de senhas e a saida
por sys.exit().

As senhas sao aleatorias, entao o teste nao fixa os caracteres sorteados: so
quantas senhas saem, em que ordem de grupo, com que tamanho e de qual
alfabeto (pontuacao, maiusculas, minusculas, digitos, pontuacao).
"""

import builtins
import string

import pytest

from LM_07 import executar

P_TAMANHO = "Enter the length of the password: "
P_ESPECIAIS = "Do you want to include special characters in the password? (y/n): "
P_MAIUSCULAS = "Do you want to include uppercase letters in the password? (y/n): "
P_MINUSCULAS = "Do you want to include lowercase letters in the password? (y/n): "
P_NUMEROS = "Do you want to include numbers in the password? (y/n): "
P_SIMBOLOS = "Do you want to include symbols in the password? (y/n): "
P_ARQUIVO = "Do you want to store the list of passwords in a text file? (y/n): "
P_PASTA = "Enter the path to the folder where you want to store the text file: "
P_MAIS = "Do you want to generate more passwords? (y/n): "


def _teclado(monkeypatch, respostas):
    """Instala o duble de input() e devolve a lista das perguntas feitas."""
    respostas, perguntas = list(respostas), []

    def falso_input(pergunta=""):
        perguntas.append(pergunta)
        if not respostas:
            raise AssertionError("a unidade pediu uma entrada que o teste nao previu: %r" % pergunta)
        return respostas.pop(0)

    monkeypatch.setattr(builtins, "input", falso_input)
    return perguntas


def _confere_senhas(senhas, tamanho, alfabetos):
    """Cada alfabeto gera `tamanho` senhas de `tamanho` caracteres, em ordem."""
    assert len(senhas) == tamanho * len(alfabetos)
    for n, senha in enumerate(senhas):
        assert len(senha) == tamanho, senha
        assert set(senha) <= set(alfabetos[n // tamanho]), senha


def test_tipico_todas_as_opcoes_sem_arquivo(monkeypatch, tmp_path, capsys):
    """Caso tipico: tamanho 3, tudo 'y', sem arquivo, e nao gera mais."""
    perguntas = _teclado(monkeypatch, ["3", "y", "y", "y", "y", "y", "n", str(tmp_path), "n"])

    with pytest.raises(SystemExit):
        executar()

    assert perguntas == [P_TAMANHO, P_ESPECIAIS, P_MAIUSCULAS, P_MINUSCULAS, P_NUMEROS,
                         P_SIMBOLOS, P_ARQUIVO, P_PASTA, P_MAIS]
    linhas = capsys.readouterr().out.split("\n")
    assert linhas[:4] == ["Welcome to the password generator!", "", "", "Here are the generated passwords:"]
    _confere_senhas(linhas[4:19], 3, [string.punctuation, string.ascii_uppercase,
                                      string.ascii_lowercase, string.digits, string.punctuation])
    assert linhas[19:] == ["", "", "", "Goodbye.", ""]
    assert list(tmp_path.iterdir()) == []


def test_borda_respostas_repetidas_e_gravacao_no_arquivo(monkeypatch, tmp_path, capsys):
    """Borda: respostas invalidas repetem a pergunta; com arquivo, pergunta de
    novo (input sem texto) e grava passwords.txt na pasta informada."""
    perguntas = _teclado(monkeypatch, [
        "abc", "2", "x", "n", "y", "y", "y", "y", "y",
        str(tmp_path / "nao_existe"), str(tmp_path),
        "z", "y", str(tmp_path), "n",
    ])

    with pytest.raises(SystemExit):
        executar()

    assert perguntas == [P_TAMANHO, P_TAMANHO, P_ESPECIAIS, P_ESPECIAIS, P_MAIUSCULAS,
                         P_MINUSCULAS, P_NUMEROS, P_SIMBOLOS, P_ARQUIVO, P_PASTA, P_PASTA,
                         "", "", P_PASTA, P_MAIS]
    linhas = capsys.readouterr().out.split("\n")
    assert linhas[:6] == ["Welcome to the password generator!", "", "Please enter a valid number.",
                          "Please enter a valid answer.", "Please enter a valid path.", ""]
    assert linhas[6] == "Here are the generated passwords:"
    senhas = linhas[7:15]
    _confere_senhas(senhas, 2, [string.ascii_uppercase, string.ascii_lowercase,
                                string.digits, string.punctuation])
    assert linhas[15:] == ["", "", P_ARQUIVO, "Please enter a valid answer.", "", "", "",
                           "The passwords have been stored in the text file.", "", "",
                           "Goodbye.", ""]
    assert (tmp_path / "passwords.txt").read_text() == "".join(s + "\n" for s in senhas)


def test_invalido_recusar_maiusculas_quebra_a_geracao(monkeypatch, tmp_path, capsys):
    """Invalido: com 'n' para maiusculas a variavel nunca e definida e a
    geracao falha depois de todas as perguntas, sem imprimir senha."""
    perguntas = _teclado(monkeypatch, ["2", "n", "n", "y", "y", "y", "n", str(tmp_path)])

    with pytest.raises(NameError):
        executar()

    assert perguntas == [P_TAMANHO, P_ESPECIAIS, P_MAIUSCULAS, P_MINUSCULAS, P_NUMEROS,
                         P_SIMBOLOS, P_ARQUIVO, P_PASTA]
    assert capsys.readouterr().out == "Welcome to the password generator!\n\n"
