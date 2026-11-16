"""Tests for instance LM-11: they pin the observable behavior of run().

Only run() is imported. What is pinned is the exact printed text for each
number of misses (8 lines per drawing) and that nothing is printed outside
0 to 6.
"""

from LM_11 import run

TOP = ["_________", "|       |"]
EMPTY = "|"


def _output(capsys):
    return capsys.readouterr().out.splitlines()


def test_typical_three_misses_head_and_arm(capsys):
    """Typical case: with 3 misses, head, torso and one arm appear."""
    run(3)
    assert _output(capsys) == TOP + ["|       O", "|      /|"] + [EMPTY] * 4


def test_edge_every_drawing_from_0_to_6(capsys):
    """Edge: the extremes (0 and 6) and each intermediate step."""
    body = [
        [],
        ["|       O"],
        ["|       O", "|       |"],
        ["|       O", "|      /|"],
        ["|       O", "|      /|\\"],
        ["|       O", "|      /|\\", "|      /"],
        ["|       O", "|      /|\\", "|      / \\"],
    ]
    for misses, parts in enumerate(body):
        run(misses)
        assert _output(capsys) == TOP + parts + [EMPTY] * (6 - len(parts)), misses


def test_invalid_outside_0_to_6_prints_nothing(capsys):
    """Invalid: 7, a negative number or text match no case and raise no error."""
    for misses in (7, -1, "3"):
        assert run(misses) is None
        assert capsys.readouterr().out == "", misses
