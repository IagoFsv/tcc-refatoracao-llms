"""Testes da instancia LM-01: fixam o comportamento observavel de executar().

So executar() e importado. Uma refatoracao pode renomear, dividir ou mover
qualquer outra funcao do arquivo sem que nada aqui quebre; o que nao pode
mudar e o que a unidade pergunta, na ordem em que pergunta, o que ela imprime
e os comandos que ela manda para o sistema.

O trecho faz I/O interativo e chama ffmpeg. Nada disso e alterado na unidade:
quem intercepta e este arquivo, trocando input() e os.system() por dubles.
"""

import builtins
import os

import pytest

from LM_01 import executar


def _preparar(monkeypatch, tmp_path, arquivos=("a.mp4", "b.mp4")):
    """Monta as pastas, instala os dubles e devolve o que o teste precisa.

    Devolve (entrada, saida, script, perguntas, comandos). O teste preenche
    `script` com as respostas na ordem em que serao pedidas; `perguntas` e
    `comandos` sao preenchidos durante a execucao.
    """
    entrada = tmp_path / "entrada"
    entrada.mkdir()
    for nome in arquivos:
        (entrada / nome).write_bytes(b"")
    saida = tmp_path / "saida"  # de proposito nao existe ainda

    script, perguntas, comandos = [], [], []

    def falso_input(pergunta=""):
        perguntas.append(pergunta)
        if not script:
            raise AssertionError(
                "a unidade pediu mais uma entrada que o teste nao previu: %r" % pergunta
            )
        return script.pop(0)

    def falso_system(comando):
        comandos.append(comando)
        return 0

    monkeypatch.setattr(builtins, "input", falso_input)
    monkeypatch.setattr(os, "system", falso_system)
    return entrada, saida, script, perguntas, comandos


def test_tipico_converte_cada_arquivo_da_pasta(monkeypatch, tmp_path, capsys):
    """Caso tipico: corte de inicio e crf informados, sem preview."""
    entrada, saida, script, perguntas, comandos = _preparar(monkeypatch, tmp_path)
    script += [str(entrada), str(saida), "00:00:01", "", "", "23", "n"]

    executar()

    assert perguntas == [
        "Enter input directory: ",
        "Enter output directory: ",
        "Enter start time (HH:MM:SS, enter nothing to skip): ",
        "Enter duration (HH:MM:SS, enter nothing to skip): ",
        "Enter crop parameters (w:h:x:y, enter nothing to skip): ",
        "Enter crf level (Enter nothing to skip): ",
        "Generate preview thumbnails? (y/n): ",
    ]
    assert sorted(comandos) == [
        "ffmpeg -y -ss 00:00:01 -i %s -crf 23 %s" % (entrada / "a.mp4", saida / "a.mp4"),
        "ffmpeg -y -ss 00:00:01 -i %s -crf 23 %s" % (entrada / "b.mp4", saida / "b.mp4"),
    ]
    assert saida.is_dir()
    assert capsys.readouterr().out == ""


def test_borda_sem_nenhuma_flag_nao_chama_ffmpeg(monkeypatch, tmp_path, capsys):
    """Borda: tudo em branco, entao nao ha o que fazer e nada e convertido."""
    entrada, saida, script, perguntas, comandos = _preparar(monkeypatch, tmp_path)
    script += [str(entrada), str(saida), "", "", "", "", ""]

    executar()

    assert comandos == []
    assert "No flags specified" in capsys.readouterr().out
    assert not saida.exists()


def test_invalido_parametros_de_corte_nao_numericos(monkeypatch, tmp_path, capsys):
    """Invalido: crop que nao converte para inteiro aborta antes de converter."""
    entrada, saida, script, perguntas, comandos = _preparar(monkeypatch, tmp_path)
    script += [str(entrada), str(saida), "00:00:01", "", "abc", ""]

    executar()

    assert comandos == []
    assert "Invalid crop parameters" in capsys.readouterr().out
    assert not saida.exists()
