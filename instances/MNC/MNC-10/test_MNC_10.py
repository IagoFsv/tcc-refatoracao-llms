"""Tests for instance MNC-10: they pin the observable behavior of run().

Only run() is imported. The test runs in a temporary folder with a
pyproject.toml and the package folder. The refactoring may reorganize the
access to the sections; what must not change is the effect: the package
folder renamed (with _ instead of -), the name in [tool.poetry] replaced by
the new one (with hyphens), the rest of pyproject.toml preserved, and the
error when there is no [tool.poetry].

pyproject.toml is compared after being parsed, not as text: the order of the
sections and the formatting come from toml.dump.
"""

import pytest
import toml

from MNC_10 import run

PYPROJECT = (
    '[tool.poetry]\nname = "my-app"\nversion = "0.1.0"\n\n'
    '[build-system]\nrequires = ["poetry-core"]\n'
)


def project(folder, content=PYPROJECT, package="my_app"):
    (folder / "pyproject.toml").write_text(content, encoding="utf-8")
    (folder / package).mkdir()
    (folder / package / "__init__.py").write_text("x = 1\n", encoding="utf-8")


def read_pyproject(folder):
    return toml.loads((folder / "pyproject.toml").read_text(encoding="utf-8"))


def test_typical_folder_and_name_renamed(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    project(tmp_path)

    run("new-app")

    assert sorted(p.name for p in tmp_path.iterdir()) == ["new_app", "pyproject.toml"]
    assert (tmp_path / "new_app" / "__init__.py").read_text(encoding="utf-8") == "x = 1\n"
    assert read_pyproject(tmp_path) == {
        "tool": {"poetry": {"name": "new-app", "version": "0.1.0"}},
        "build-system": {"requires": ["poetry-core"]},
    }


def test_edge_name_without_hyphen_and_several_hyphens(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    project(tmp_path, '[tool.poetry]\nname = "app"\n', package="app")

    run("app-for-test-2")

    assert sorted(p.name for p in tmp_path.iterdir()) == ["app_for_test_2", "pyproject.toml"]
    assert read_pyproject(tmp_path) == {"tool": {"poetry": {"name": "app-for-test-2"}}}


def test_invalid_no_tool_poetry_section(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    project(tmp_path, '[project]\nname = "my-app"\n')

    with pytest.raises(KeyError):
        run("new-app")
