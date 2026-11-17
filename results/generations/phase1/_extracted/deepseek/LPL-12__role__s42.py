"""Interpolation of two (x, y) series on the same set of equally spaced x.

Public entry point: run(data1, data2, interval). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


def interpolate_df_at_fixed_x_intervals(params):
    """
    Interpolate dataframes at fixed x intervals.
    """

    x1, y1, x2, y2, x_interval = params

    x_min = min(x1.min(), x2.min())
    x_max = max(x1.max(), x2.max())

    # Create a new set of x values at fixed intervals
    x_new = np.arange(x_min, x_max + x_interval, x_interval)
    x_new = pd.Series(x_new)

    # Create interpolated y values for each set of data at the new x values
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
    x1, y1 = data1.iloc[:, 0], data1.iloc[:, 1]
    x2, y2 = data2.iloc[:, 0], data2.iloc[:, 1]
    params = (x1, y1, x2, y2, interval)
    return interpolate_df_at_fixed_x_intervals(params)
