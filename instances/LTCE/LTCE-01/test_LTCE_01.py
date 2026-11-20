"""Tests for instance LTCE-01: they pin the observable behavior of run().

Only run() is imported. run executes the unit file as a program (__main__
block) with the given command-line arguments. The tests run in a temporary
folder with chat exports. The refactoring may reorganize the main block
(including moving it into a function called under the same guard) and
replace the conditional expressions with if statements; what must not
change is how the arguments are read, the defaults, the output written, the
messages printed and the errors.

Paths are given with forward slashes, as the program splits them on "/".
The tests pin the behavior as it is, including the defects of the original:
a verbose value other than true/t stays a (truthy) string, and only the
parent of the output folder is created, not the folder itself.
"""

import json
import os

import pytest

from LTCE_01 import run


def export(folder, name, messages):
    os.makedirs(folder, exist_ok=True)
    data = {"messages": [{"author": {"name": a, "discriminator": d}, "content": c} for a, d, c in messages]}
    with open(os.path.join(folder, name), "w", encoding="utf-8") as file:
        json.dump(data, file)


def read(path):
    with open(path, encoding="utf-8") as file:
        return file.read()


@pytest.fixture
def folder(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    export("chats", "b.json", [("Bia", "0002", "bye")])
    export("chats", "a.json", [("Ana", "0420", "hi\nthere"), ("Rui", "0007", "")])
    export("JSON Files", "c.json", [("Caio", "1111", "default input")])
    return tmp_path


def test_typical_input_and_output_options(folder, capsys):
    os.makedirs("out/day")

    run(["-i", "chats", "-o", "out/day/result.txt"])

    assert read("out/day/result.txt") == "Ana___0420: hi\nAna___0420: there\nBia___0002: bye"
    assert capsys.readouterr().out == ""
    run(["--input", "chats", "--output", "out/day/long.txt", "--verbose", "t"])
    printed = capsys.readouterr().out
    assert "Running the program..." in printed and "Program finished successfully!" in printed
    assert read("out/day/long.txt") == read("out/day/result.txt")


def test_edge_defaults_help_verbose_string_and_output_folders(folder, capsys):
    os.makedirs("Output")
    run([])
    assert read("Output/output.txt") == "Caio___1111: default input"

    with pytest.raises(SystemExit):
        run(["-o", "x.txt", "--help"])
    printed = capsys.readouterr().out
    assert "Combine and convert exports from Discord" in printed
    assert "JSON Files" in printed

    os.makedirs("out/day")
    run(["-i", "chats", "-o", "out/day/v.txt", "-v", "false"])  # "false" stays a truthy string
    assert "Running the program..." in capsys.readouterr().out

    with pytest.raises(FileNotFoundError):  # creates only "made", not "made/day"
        run(["-i", "chats", "-o", "made/day/result.txt"])
    assert os.path.isdir("made") and not os.path.exists("made/day")


def test_invalid_option_without_value(folder):
    with pytest.raises(IndexError):
        run(["-o", "out/result.txt", "-i"])
