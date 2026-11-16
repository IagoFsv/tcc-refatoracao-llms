"""Tests for instance LM-07: they pin the observable behavior of run().

Only run() is imported. What is pinned is what the generator asks, in the
order it asks, the text it prints, the passwords file and the exit through
sys.exit().

The passwords are random, so the test does not pin the drawn characters:
only how many passwords come out, in which group order, with which length
and from which alphabet (punctuation, uppercase, lowercase, digits,
punctuation).
"""

import builtins
import string

import pytest

from LM_07 import run

P_LENGTH = "Enter the length of the password: "
P_SPECIAL = "Do you want to include special characters in the password? (y/n): "
P_UPPER = "Do you want to include uppercase letters in the password? (y/n): "
P_LOWER = "Do you want to include lowercase letters in the password? (y/n): "
P_NUMBERS = "Do you want to include numbers in the password? (y/n): "
P_SYMBOLS = "Do you want to include symbols in the password? (y/n): "
P_FILE = "Do you want to store the list of passwords in a text file? (y/n): "
P_FOLDER = "Enter the path to the folder where you want to store the text file: "
P_MORE = "Do you want to generate more passwords? (y/n): "


def _keyboard(monkeypatch, answers):
    """Installs the input() double and returns the list of prompts."""
    answers, prompts = list(answers), []

    def fake_input(prompt=""):
        prompts.append(prompt)
        if not answers:
            raise AssertionError("the unit asked for an input the test did not expect: %r" % prompt)
        return answers.pop(0)

    monkeypatch.setattr(builtins, "input", fake_input)
    return prompts


def _check_passwords(passwords, length, alphabets):
    """Each alphabet generates `length` passwords of `length` characters, in order."""
    assert len(passwords) == length * len(alphabets)
    for n, password in enumerate(passwords):
        assert len(password) == length, password
        assert set(password) <= set(alphabets[n // length]), password


def test_typical_all_options_without_file(monkeypatch, tmp_path, capsys):
    """Typical case: length 3, all 'y', no file, and no more passwords."""
    prompts = _keyboard(monkeypatch, ["3", "y", "y", "y", "y", "y", "n", str(tmp_path), "n"])

    with pytest.raises(SystemExit):
        run()

    assert prompts == [P_LENGTH, P_SPECIAL, P_UPPER, P_LOWER, P_NUMBERS,
                       P_SYMBOLS, P_FILE, P_FOLDER, P_MORE]
    lines = capsys.readouterr().out.split("\n")
    assert lines[:4] == ["Welcome to the password generator!", "", "", "Here are the generated passwords:"]
    _check_passwords(lines[4:19], 3, [string.punctuation, string.ascii_uppercase,
                                      string.ascii_lowercase, string.digits, string.punctuation])
    assert lines[19:] == ["", "", "", "Goodbye.", ""]
    assert list(tmp_path.iterdir()) == []


def test_edge_repeated_answers_and_writing_the_file(monkeypatch, tmp_path, capsys):
    """Edge: invalid answers repeat the prompt; with a file, it asks again
    (input without text) and writes passwords.txt in the given folder."""
    prompts = _keyboard(monkeypatch, [
        "abc", "2", "x", "n", "y", "y", "y", "y", "y",
        str(tmp_path / "does_not_exist"), str(tmp_path),
        "z", "y", str(tmp_path), "n",
    ])

    with pytest.raises(SystemExit):
        run()

    assert prompts == [P_LENGTH, P_LENGTH, P_SPECIAL, P_SPECIAL, P_UPPER,
                       P_LOWER, P_NUMBERS, P_SYMBOLS, P_FILE, P_FOLDER, P_FOLDER,
                       "", "", P_FOLDER, P_MORE]
    lines = capsys.readouterr().out.split("\n")
    assert lines[:6] == ["Welcome to the password generator!", "", "Please enter a valid number.",
                         "Please enter a valid answer.", "Please enter a valid path.", ""]
    assert lines[6] == "Here are the generated passwords:"
    passwords = lines[7:15]
    _check_passwords(passwords, 2, [string.ascii_uppercase, string.ascii_lowercase,
                                    string.digits, string.punctuation])
    assert lines[15:] == ["", "", P_FILE, "Please enter a valid answer.", "", "", "",
                          "The passwords have been stored in the text file.", "", "",
                          "Goodbye.", ""]
    assert (tmp_path / "passwords.txt").read_text() == "".join(p + "\n" for p in passwords)


def test_invalid_refusing_uppercase_breaks_generation(monkeypatch, tmp_path, capsys):
    """Invalid: with 'n' for uppercase the variable is never defined and
    generation fails after all the prompts, without printing any password."""
    prompts = _keyboard(monkeypatch, ["2", "n", "n", "y", "y", "y", "n", str(tmp_path)])

    with pytest.raises(NameError):
        run()

    assert prompts == [P_LENGTH, P_SPECIAL, P_UPPER, P_LOWER, P_NUMBERS,
                       P_SYMBOLS, P_FILE, P_FOLDER]
    assert capsys.readouterr().out == "Welcome to the password generator!\n\n"
