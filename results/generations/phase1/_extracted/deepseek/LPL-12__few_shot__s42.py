"""Interpolation of two (x, y) series on the same set of equally spaced x.

Public entry point: run(data1, data2, interval). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from dataclasses import dataclass, asdict

@dataclass
class Data:
    x: pd.Series
    y: pd.Series

@dataclass
class Interval:
    value: float

def interpolate_df_at_fixed_x_intervals(data1: Data, data2: Data, interval: Interval):
    """
    Interpolate dataframes at fixed x intervals.
    """

    x_min = min(data1.x.min(), data2.x.min())
    x_max = max(data1.x.max(), data2.x.max())

    # Create a new set of x values at fixed intervals
    x_new = np.arange(x_min, x_max + interval.value, interval.value)
    x_new = pd.Series(x_new)

    # Create interpolated y values for each set of data at the new x values
    interpolation_func1 = interp1d(data1.x, data1.y, kind='linear', fill_value='extrapolate')
    interpolation_func2 = interp1d(data2.x, data2.y, kind='linear', fill_value='extrapolate')
    y1_new = interpolation_func1(x_new)
    y2_new = interpolation_func2(x_new)
    y_diff = y1_new - y2_new

    df_interpolated = pd.DataFrame({
        "x1_new": x_new,
        "y1_new": y1_new,
        "y2_new": y2_new,
        "y_diff": y_diff
    })

    return df_interpolated


def run(data1: Data, data2: Data, interval: Interval):
    """data1 and data2: DataFrames with the x column first and the y column second. Public entry point of this unit."""
    return interpolate_df_at_fixed_x_intervals(data1, data2, interval)
