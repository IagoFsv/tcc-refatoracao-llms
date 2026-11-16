"""Tests for instance LPL-12: they pin the observable behavior of run().

Only run() is imported. The refactoring may group the parameters of
interpolate_df_at_fixed_x_intervals into an object, change the signature or
split the function, as long as it updates the call inside the unit; what
must not change are the columns (names derived from the input series, and
y_diff), the interpolated and extrapolated values and the error on a zero
interval.

Arithmetic of the typical test: y1 = 2x at the given points. y2 goes through
(1.5, 3), (2.5, 5) and (3.5, 8): slope 2 on the first segment and 3 on the
last; outside the range, it extrapolates with the end segment. At
x = 1, 2, 3, 4, 5: y2 = 2, 4, 6.5, 9.5, 12.5 and
y_diff = y1 - y2 = 0, 0, -0.5, -1.5, -2.5.
"""

import pandas as pd
import pytest

from LPL_12 import run

DATA1 = pd.DataFrame({"x1": [1, 2, 3, 4, 5], "y1": [2, 4, 6, 8, 10]})
DATA2 = pd.DataFrame({"x2": [1.5, 2.5, 3.5], "y2": [3, 5, 8]})


def _expected(xs, y1, y2):
    return pd.DataFrame({
        "x1_new": xs,
        "y1_new": y1,
        "y2_new": y2,
        "y_diff": [a - b for a, b in zip(y1, y2)],
    })


def test_typical_interval_one_with_extrapolation_at_the_ends():
    result = run(DATA1, DATA2, 1.0)

    expected = _expected([1.0, 2.0, 3.0, 4.0, 5.0], [2.0, 4.0, 6.0, 8.0, 10.0],
                         [2.0, 4.0, 6.5, 9.5, 12.5])
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


def test_edge_interval_larger_than_the_range_goes_past_the_maximum():
    # x goes from 1 to 5 + 10 (exclusive), in steps of 10: the second point,
    # 11, lies beyond the largest x and is extrapolated.
    result = run(DATA1, DATA2, 10)

    expected = _expected([1, 11], [2.0, 22.0], [2.0, 30.5])
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


def test_invalid_zero_interval():
    # x_min and x_max are numpy scalars, and np.arange with a zero step raises
    # ValueError (with plain Python numbers it would be ZeroDivisionError).
    with pytest.raises(ValueError):
        run(DATA1, DATA2, 0)
