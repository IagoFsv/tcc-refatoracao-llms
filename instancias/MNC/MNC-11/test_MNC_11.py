"""Testes da instancia MNC-11: fixam o comportamento observavel de executar().

So executar() e importado. O teste roda numa pasta temporaria com um
pyproject.toml; os comandos nao rodam de verdade, executar devolve o que foi
pedido (comando, argumentos e versao gravada no arquivo naquele momento). A
refatoracao pode reorganizar o acesso as secoes e a restauracao do arquivo;
o que nao pode mudar e: durante o build a versao gravada e a nova, o comando
e os argumentos sao os mesmos, e no fim o pyproject.toml volta ao texto
original, tanto no sucesso quanto na falha (que e repassada).
"""

import pytest
from invoke.exceptions import UnexpectedExit

from MNC_11 import executar

PYPROJECT = (
    '[tool.poetry]\nname = "ai-shell"\nversion = "0.1.0"\n\n'
    '[build-system]\nrequires = ["poetry-core"]\n'
)
COMANDO = (
    "\n"
    "                poetry build --no-interaction\n"
    "                poetry publish --no-interaction\n"
    "            "
)


def test_tipico_build_com_versao_nova_e_arquivo_restaurado(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "pyproject.toml").write_text(PYPROJECT, encoding="utf-8")

    comandos = executar("2.0.0")

    assert comandos == [(COMANDO, {"pty": True}, "2.0.0")]
    assert (tmp_path / "pyproject.toml").read_text(encoding="utf-8") == PYPROJECT


def test_borda_falha_na_publicacao_restaura_e_repassa_o_erro(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "pyproject.toml").write_text(PYPROJECT, encoding="utf-8")

    with pytest.raises(UnexpectedExit):
        executar("2.1.0", falhar_publicacao=True)

    assert (tmp_path / "pyproject.toml").read_text(encoding="utf-8") == PYPROJECT


def test_invalido_sem_secao_tool_poetry(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    original = '[project]\nname = "ai-shell"\n'
    (tmp_path / "pyproject.toml").write_text(original, encoding="utf-8")

    with pytest.raises(KeyError):
        executar("2.0.0")
    assert (tmp_path / "pyproject.toml").read_text(encoding="utf-8") == original
