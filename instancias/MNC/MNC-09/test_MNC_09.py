"""Testes da instancia MNC-09: fixam o comportamento observavel de executar().

So executar() e importado. O teste roda numa pasta temporaria com um
pyproject.toml. A refatoracao pode reorganizar a leitura das secoes; o que
nao pode mudar e o nome devolvido (o de [tool.poetry], com _ no lugar de -)
e o erro quando o arquivo nao tem a secao [tool.poetry].
"""

import pytest

from MNC_09 import executar


def pyproject(pasta, conteudo):
    (pasta / "pyproject.toml").write_text(conteudo, encoding="utf-8")


def test_tipico_nome_com_hifen_vira_sublinhado(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    pyproject(tmp_path, '[tool.poetry]\nname = "ai-shell"\nversion = "0.1.0"\n')

    assert executar() == "ai_shell"


def test_borda_varios_hifens_sublinhado_mantido_e_outras_secoes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    pyproject(tmp_path, '[project]\nname = "outro"\n\n[tool.poetry]\nname = "a-b_c-d"\n')
    assert executar() == "a_b_c_d"

    pyproject(tmp_path, '[tool.poetry]\nname = "simples"\n')
    assert executar() == "simples"


def test_invalido_sem_secao_tool_poetry(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    pyproject(tmp_path, '[project]\nname = "ai-shell"\n')

    with pytest.raises(KeyError):
        executar()
