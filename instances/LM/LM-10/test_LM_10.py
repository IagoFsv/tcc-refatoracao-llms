"""Tests for instance LM-10: they pin the observable behavior of run().

Only run() is imported. What is pinned is what the calculator asks, in the
order it asks, and the exact text it prints, including when the user asks
to calculate again.

The unit reads from the keyboard with input(); this file answers, replacing
input() with a double that holds the answers in order.
"""

import builtins

import pytest

from LM_10 import run

MENU = ("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n"
        " 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n"
        " 6 for calories needed to maintain weight \n"
        " 7. for calculating everything from bmi and activity level\n Enter your choice: ")
ACTIVITY = ("What is your activity level? Sedentary = 1.2, lightly active = 1.375, "
            "moderately active = 1.55, very active = 1.725, extra active = 1.9")
AGAIN = "Do you want to calculate again? y/n: "
DASHES = "-" * 40
WEIGHT, HEIGHT_CM, AGE = "What is your weight in kg?", "What is your height in cm?", "What is your age in years?"


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


def test_typical_option_7_computes_everything(monkeypatch, capsys):
    """Typical case: option 7 with 70 kg, 175 cm, 30 years and activity 2."""
    prompts = _keyboard(monkeypatch, ["7", "70", "175", "30", "2", "n"])

    run()

    assert prompts == [MENU, "what is your weight in kg?", "what is your height in cm?",
                       "what is your age in years?", ACTIVITY, AGAIN]
    assert capsys.readouterr().out.splitlines() == [
        "Your BMI is 22.857142857142858",
        "Your bmr is 1643.75",
        "Your tdee is 3287.5",
        "You need 2787.5 calories to lose weight",
        "You need 3787.5 calories to gain weight",
        "You need 3287.5 calories to maintain weight",
        DASHES,
        "Goodbye, See You on The Other Side!",
        DASHES,
    ]


def test_edge_calculating_again_goes_through_the_options_and_ends_on_an_invalid_option(monkeypatch, capsys):
    """Edge: 'y' restarts the menu; it goes through 1, 2, 4, 5 and 6 and stops at option 9."""
    measures = ["70", "175", "30"]
    prompts = _keyboard(monkeypatch, ["1", "70", "2", "y",
                                      "2", *measures, "y",
                                      "4", *measures, "2", "y",
                                      "5", *measures, "2", "y",
                                      "6", *measures, "2", "y",
                                      "9"])

    run()

    again = [DASHES, "Sure, let's do it again", DASHES]
    assert capsys.readouterr().out.splitlines() == [
        "Your BMI is 17.5", *again,
        "Your bmr is 1643.75", *again,
        "You need 2787.5 calories to lose weight", *again,
        "You need 3787.5 calories to gain weight", *again,
        "You need 3287.5 calories to maintain weight", *again,
        "Invalid number, choose a wise one next time",
    ]
    three = [WEIGHT, HEIGHT_CM, AGE]
    assert prompts == [MENU, WEIGHT, "What is your height in meters?", AGAIN,
                       MENU, *three, AGAIN,
                       MENU, *three, ACTIVITY, AGAIN,
                       MENU, *three, ACTIVITY, AGAIN,
                       MENU, *three, ACTIVITY, AGAIN,
                       MENU]


def test_invalid_decimal_activity_level(monkeypatch, capsys):
    """Invalid: the prompt suggests 1.2, but the answer is read with int()."""
    prompts = _keyboard(monkeypatch, ["3", "70", "175", "30", "1.2"])

    with pytest.raises(ValueError):
        run()

    assert prompts == [MENU, WEIGHT, HEIGHT_CM, AGE, ACTIVITY]
    assert capsys.readouterr().out == ""
