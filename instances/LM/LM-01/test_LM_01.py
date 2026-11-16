"""Tests for instance LM-01: they pin the observable behavior of run().

Only run() is imported. A refactoring may rename, split or move any other
function in the file without breaking anything here; what must not change is
what the unit asks, in the order it asks, what it prints and the commands it
sends to the system.

The code does interactive I/O and calls ffmpeg. None of that is changed in
the unit: this file intercepts it, replacing input() and os.system() with
test doubles.
"""

import builtins
import os

import pytest

from LM_01 import run


def _prepare(monkeypatch, tmp_path, files=("a.mp4", "b.mp4")):
    """Builds the folders, installs the doubles and returns what the test needs.

    Returns (input_dir, output_dir, script, prompts, commands). The test fills
    `script` with the answers in the order they will be asked; `prompts` and
    `commands` are filled during the run.
    """
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    for name in files:
        (input_dir / name).write_bytes(b"")
    output_dir = tmp_path / "output"  # deliberately does not exist yet

    script, prompts, commands = [], [], []

    def fake_input(prompt=""):
        prompts.append(prompt)
        if not script:
            raise AssertionError(
                "the unit asked for one more input that the test did not expect: %r" % prompt
            )
        return script.pop(0)

    def fake_system(command):
        commands.append(command)
        return 0

    monkeypatch.setattr(builtins, "input", fake_input)
    monkeypatch.setattr(os, "system", fake_system)
    return input_dir, output_dir, script, prompts, commands


def test_typical_converts_each_file_in_the_folder(monkeypatch, tmp_path, capsys):
    """Typical case: start time and crf given, no preview."""
    input_dir, output_dir, script, prompts, commands = _prepare(monkeypatch, tmp_path)
    script += [str(input_dir), str(output_dir), "00:00:01", "", "", "23", "n"]

    run()

    assert prompts == [
        "Enter input directory: ",
        "Enter output directory: ",
        "Enter start time (HH:MM:SS, enter nothing to skip): ",
        "Enter duration (HH:MM:SS, enter nothing to skip): ",
        "Enter crop parameters (w:h:x:y, enter nothing to skip): ",
        "Enter crf level (Enter nothing to skip): ",
        "Generate preview thumbnails? (y/n): ",
    ]
    assert sorted(commands) == [
        "ffmpeg -y -ss 00:00:01 -i %s -crf 23 %s" % (input_dir / "a.mp4", output_dir / "a.mp4"),
        "ffmpeg -y -ss 00:00:01 -i %s -crf 23 %s" % (input_dir / "b.mp4", output_dir / "b.mp4"),
    ]
    assert output_dir.is_dir()
    assert capsys.readouterr().out == ""


def test_edge_no_flags_does_not_call_ffmpeg(monkeypatch, tmp_path, capsys):
    """Edge: everything blank, so there is nothing to do and nothing is converted."""
    input_dir, output_dir, script, prompts, commands = _prepare(monkeypatch, tmp_path)
    script += [str(input_dir), str(output_dir), "", "", "", "", ""]

    run()

    assert commands == []
    assert "No flags specified" in capsys.readouterr().out
    assert not output_dir.exists()


def test_invalid_non_numeric_crop_parameters(monkeypatch, tmp_path, capsys):
    """Invalid: a crop that does not convert to int aborts before converting."""
    input_dir, output_dir, script, prompts, commands = _prepare(monkeypatch, tmp_path)
    script += [str(input_dir), str(output_dir), "00:00:01", "", "abc", ""]

    run()

    assert commands == []
    assert "Invalid crop parameters" in capsys.readouterr().out
    assert not output_dir.exists()
