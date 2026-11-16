"""Tests for instance MNC-09: they pin the observable behavior of run().

Only run() is imported. The test runs in a temporary folder with a
pyproject.toml. The refactoring may reorganize how the sections are read;
what must not change is the returned name (the one in [tool.poetry], with _
instead of -) and the error when the file has no [tool.poetry] section.
"""

import pytest

from MNC_09 import run


def pyproject(folder, content):
    (folder / "pyproject.toml").write_text(content, encoding="utf-8")


def test_typical_name_with_hyphen_becomes_underscore(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    pyproject(tmp_path, '[tool.poetry]\nname = "ai-shell"\nversion = "0.1.0"\n')

    assert run() == "ai_shell"


def test_edge_several_hyphens_underscore_kept_and_other_sections(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    pyproject(tmp_path, '[project]\nname = "other"\n\n[tool.poetry]\nname = "a-b_c-d"\n')
    assert run() == "a_b_c_d"

    pyproject(tmp_path, '[tool.poetry]\nname = "simple"\n')
    assert run() == "simple"


def test_invalid_no_tool_poetry_section(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    pyproject(tmp_path, '[project]\nname = "ai-shell"\n')

    with pytest.raises(KeyError):
        run()
