"""Tests for instance LPL-14: they pin the observable behavior of run().

Only run() is imported. The refactoring may group the parameters of
simulate_bouncing_ball into objects (initial state, time, physics), change
the signature or split the function, as long as it updates the call inside
the unit; what must not change are the returned positions, the default
values of restitution (0.2) and gravity (9.83) and the error on a non-integer
number of steps.

Peculiarity of the original, pinned as it is: when the ball does not go past
the floor, the y position receives vy * dt twice in the same step, and the
stored y may become negative (the bounce only happens in the next step).

Arithmetic of the typical test (x0=0, y0=0.3, vx=1, vy=-2, dt=0.1,
restitution 0.5, g=10):
  step 1: y = 0.3 - 0.2 = 0.1 (not negative) -> y = 0.1 - 0.2 = -0.1;
          vy = -2 - 1 = -3
  step 2: y = -0.1 - 0.3 = -0.4 (negative) -> bounces: vy = 1.5, y = 0
  step 3: y = 0 + 0.15 = 0.15 -> y = 0.15 + 0.15 = 0.3; vy = 0.5

Arithmetic of the edge test (at rest on the floor, default values, dt=0.1):
  step 1: y = 0 (not negative) -> y = 0; vy = -0.983
  step 2: y = -0.0983 (negative) -> bounces: vy = 0.983 * 0.2 = 0.1966, y = 0
  step 3: y = 0.01966 -> y = 0.03932
"""

import pytest

from LPL_14 import run


def test_typical_ball_falls_goes_below_the_floor_and_bounces():
    xs, ys = run((0, 0.3, 1, -2), (3, 0.1), (0.5, 10))

    assert xs == pytest.approx([0, 0.1, 0.2, 0.3])
    assert ys == pytest.approx([0.3, -0.1, 0, 0.3])


def test_edge_at_rest_on_the_floor_with_default_values():
    xs, ys = run((0, 0, 0, 0), (3, 0.1))

    assert xs == pytest.approx([0, 0, 0, 0])
    assert ys == pytest.approx([0, 0, 0, 0.03932])

    xs, ys = run((2, 5, 1, 1), (0, 0.1))  # zero steps: only the initial position

    assert xs == [2]
    assert ys == [5]


def test_invalid_non_integer_number_of_steps():
    with pytest.raises(TypeError):
        run((0, 1, 1, 0), (2.5, 0.1))
