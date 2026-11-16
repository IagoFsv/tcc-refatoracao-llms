"""Tests for instance LM-04: they pin the observable behavior of run().

Only run() is imported. What is pinned is the exact printed text (with the
ANSI color and cursor codes), the pauses requested from time.sleep(), the
prompts and what the room returns, or the exit through exit().

The unit reads from the keyboard with input() and pauses with time.sleep();
this file answers, replacing both with test doubles. The opening sentence of
the rooms after the first one is drawn from four; the test accepts any of
them, without pinning how the draw is made.
"""

import builtins
import time

import pytest

from LM_04 import run

CLEAR_SCREEN, CLEAR_LINE, CLEAR_REST = "\033[2J\033[0;0f", "\033[K", "\033[J"
SENTENCES = ["What do you want to do?", "What's next?", "Now what?", "And now?"]
FOOTER = "\nh: hint\nq: quit\n\n"
WAIT = CLEAR_LINE + CLEAR_REST


def _prepare(monkeypatch, answers):
    """Installs the doubles; returns (prompts, pauses)."""
    answers, prompts, pauses = list(answers), [], []

    def fake_input(prompt=""):
        prompts.append(prompt)
        if not answers:
            raise AssertionError("the unit asked for an input the test did not expect: %r" % prompt)
        return answers.pop(0)

    monkeypatch.setattr(builtins, "input", fake_input)
    monkeypatch.setattr(time, "sleep", pauses.append)
    return prompts, pauses


def test_typical_first_room_turns_on_the_light(monkeypatch, capsys):
    """Typical case: first room, option 4 leads to another room."""
    prompts, pauses = _prepare(monkeypatch, ["4"])

    assert run("basement_dark", "", True) == ["basement_light", "The lights are now on."]

    assert prompts == ["Enter your choice: "]
    assert pauses == [0.5]
    assert capsys.readouterr().out == (
        CLEAR_SCREEN + "\033[1;4;96mBASEMENT STORAGE ROOM\033[0m\r\n\n"
        "You're not sure how you got here. It is quite dark and there's water dripping in the distance.  \n"
        "There's a door to your left and a door to your right.  There's also a chest in the corner with a \n"
        "strange hum coming from it.\n"
        "\n"
        "What do you want to do?\r\n\n"
        "1. Open the left door\n2. Open the right door\n3. Open the chest\n"
        "4. Flick the light switch on the wall\n"
        + FOOTER + WAIT
    )


def test_edge_hint_out_of_range_answers_action_that_stays_and_quit(monkeypatch, capsys):
    """Edge: room without description, with a previous message; 'h' shows the
    hint, 9 and 'x' are refused, option 2 only shows its message and 'q' quits."""
    prompts, pauses = _prepare(monkeypatch, ["h", "9", "x", "2", "q"])

    assert run("upstairs_unlocked", "A click.", False) == ["player_quits", ""]

    assert prompts == ["Enter your choice: "] * 5
    assert pauses == [1]
    body = (
        "\n"
        "{sentence}\r\n\n"
        "1. Open the front door\n2. Check out the grandfather clock\n3. Open the closet\n"
        "4. Go back downstairs\n5. Play the piano\n"
        + FOOTER
        + WAIT + "\r\n\033[0;0;32mA click by the front door?  You're almost there.  "
          "Only one thing left to do!\033[0m\n\033[3A"
        + WAIT + "\r\n\033[1;0;91mPlease enter a number between 1 and 5.\033[0m\r\n\n\033[4A"
        + WAIT + "\r\n\033[1;0;91m\033[0m\r\n\n\033[4A"
        + WAIT + "\n\033[1;0;94mThe clock appears to be broken.\033[0m\n\033[3A"
        + WAIT
    )
    head = (CLEAR_SCREEN + "\033[1;4;96mUPSTAIRS LIVING ROOM\033[0m\r\n\n"
            "\033[0;0;33mA click.\033[0m\r\n\n")
    assert capsys.readouterr().out in [head + body.format(sentence=s) for s in SENTENCES]


def test_invalid_nonexistent_room_ends_the_program(monkeypatch, capsys):
    """Invalid: a room that does not exist shows the error and calls exit()."""
    prompts, pauses = _prepare(monkeypatch, [])

    with pytest.raises(SystemExit):
        run("nonexistent_room", "", True)

    assert prompts == [] and pauses == []
    assert capsys.readouterr().out == (
        "\r\n\033[1;0;91mProgram error: Room nonexistent_room not found.  "
        "Aborting game.\033[0m\r\n\n"
    )
