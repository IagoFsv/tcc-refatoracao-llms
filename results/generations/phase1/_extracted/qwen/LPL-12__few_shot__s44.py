"""Interpolation of two (x, y) series on the same set of equally spaced x.

Public entry point: run(data1, data2, interval). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


class InterpolationData:
    def __init__(self, data1, data2, interval):
        self.x1, self.y1 = data1.iloc[:, 0], data1.iloc[:, 1]
        self.x2, self.y2 = data2.iloc[:, 0], data2.iloc[:, 1]
        self.interval = interval


def interpolate_df_at_fixed_x_intervals(data):
    """
    Interpolate dataframes at fixed x intervals.
    """
    x1, y1 = data.x1, data.y1
    x2, y2 = data.x2, data.y2
    interval = data.interval

    x_min = min(x1.min(), x2.min())
    x_max = max(x1.max(), x2.max())

    # Create a new set of x values at fixed intervals
    x_new = np.arange(x_min, x_max + interval, interval)
    x_new = pd.Series(x_new)

    interpolation_func1 = interp1d(x1, y1, kind='linear', fill_value='extrapolate')
    interpolation_func2 = interp1d(x2, y2, kind='linear', fill_value='extrapolate')
    y1_new = interpolation_func1(x_new)
    y2_new = interpolation_func2(x_new)
    y_diff = y1_new - y2_new

    df_interpolated = pd.DataFrame({
        x1.name + "_new": x_new,
        y1.name + "_new": y1_new,
        y2.name + "_new": y2_new,
        "y_diff": y_diff
    })

    return df_interpolated


def run(data1, data2, interval):
    """data1 and data2: DataFrames with the x column first and the y column second. Public entry point of this unit."""
    return interpolate_df_at_fixed_x_intervals(InterpolationData(data1, data2, interval))
