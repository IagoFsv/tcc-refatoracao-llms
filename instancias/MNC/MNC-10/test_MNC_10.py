"""Testes da instancia MNC-10: fixam o comportamento observavel de executar().

So executar() e importado. O teste roda numa pasta temporaria com um
pyproject.toml e a pasta do pacote. A refatoracao pode reorganizar o acesso
as secoes; o que nao pode mudar e o efeito: a pasta do pacote renomeada (com
_ no lugar de -), o nome em [tool.poetry] trocado pelo novo (com hifens), o
resto do pyproject.toml preservado, e o erro quando nao ha [tool.poetry].

O pyproject.toml e comparado depois de lido, nao como texto: a ordem das
secoes e a formatacao vem do toml.dump.
"""

import pytest
import toml

from MNC_10 import executar

PYPROJECT = (
    '[tool.poetry]\nname = "meu-app"\nversion = "0.1.0"\n\n'
    '[build-system]\nrequires = ["poetry-core"]\n'
)


def projeto(pasta, conteudo=PYPROJECT, pacote="meu_app"):
    (pasta / "pyproject.toml").write_text(conteudo, encoding="utf-8")
    (pasta / pacote).mkdir()
    (pasta / pacote / "__init__.py").write_text("x = 1\n", encoding="utf-8")


def ler_pyproject(pasta):
    return toml.loads((pasta / "pyproject.toml").read_text(encoding="utf-8"))


def test_tipico_pasta_e_nome_renomeados(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    projeto(tmp_path)

    executar("novo-app")

    assert sorted(p.name for p in tmp_path.iterdir()) == ["novo_app", "pyproject.toml"]
    assert (tmp_path / "novo_app" / "__init__.py").read_text(encoding="utf-8") == "x = 1\n"
    assert ler_pyproject(tmp_path) == {
        "tool": {"poetry": {"name": "novo-app", "version": "0.1.0"}},
        "build-system": {"requires": ["poetry-core"]},
    }


def test_borda_nome_sem_hifen_e_varios_hifens(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    projeto(tmp_path, '[tool.poetry]\nname = "app"\n', pacote="app")

    executar("app-de-teste-2")

    assert sorted(p.name for p in tmp_path.iterdir()) == ["app_de_teste_2", "pyproject.toml"]
    assert ler_pyproject(tmp_path) == {"tool": {"poetry": {"name": "app-de-teste-2"}}}


def test_invalido_sem_secao_tool_poetry(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    projeto(tmp_path, '[project]\nname = "meu-app"\n')

    with pytest.raises(KeyError):
        executar("novo-app")
