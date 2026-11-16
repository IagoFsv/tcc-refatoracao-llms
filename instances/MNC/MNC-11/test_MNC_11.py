"""Tests for instance MNC-11: they pin the observable behavior of run().

Only run() is imported. The test runs in a temporary folder with a
pyproject.toml; the commands do not run for real, run returns what was
requested (command, arguments and the version written to the file at that
moment). The refactoring may reorganize the access to the sections and the
restoration of the file; what must not change is: during the build the
written version is the new one, the command and the arguments are the same,
and at the end pyproject.toml goes back to the original text, both on
success and on failure (which is propagated).
"""

import pytest
from invoke.exceptions import UnexpectedExit

from MNC_11 import run

PYPROJECT = (
    '[tool.poetry]\nname = "ai-shell"\nversion = "0.1.0"\n\n'
    '[build-system]\nrequires = ["poetry-core"]\n'
)
COMMAND = (
    "\n"
    "                poetry build --no-interaction\n"
    "                poetry publish --no-interaction\n"
    "            "
)


def test_typical_build_with_new_version_and_file_restored(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "pyproject.toml").write_text(PYPROJECT, encoding="utf-8")

    commands = run("2.0.0")

    assert commands == [(COMMAND, {"pty": True}, "2.0.0")]
    assert (tmp_path / "pyproject.toml").read_text(encoding="utf-8") == PYPROJECT


def test_edge_publish_failure_restores_and_propagates_the_error(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "pyproject.toml").write_text(PYPROJECT, encoding="utf-8")

    with pytest.raises(UnexpectedExit):
        run("2.1.0", fail_publish=True)

    assert (tmp_path / "pyproject.toml").read_text(encoding="utf-8") == PYPROJECT


def test_invalid_no_tool_poetry_section(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    original = '[project]\nname = "ai-shell"\n'
    (tmp_path / "pyproject.toml").write_text(original, encoding="utf-8")

    with pytest.raises(KeyError):
        run("2.0.0")
    assert (tmp_path / "pyproject.toml").read_text(encoding="utf-8") == original
