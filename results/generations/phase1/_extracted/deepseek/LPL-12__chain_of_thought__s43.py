"""Interpolation of two  (x, y) series on the same set of equally spaced x.

Public entry point: run(data1, data2, interval). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


class InterpolationParams:
    def __init__(self, x1, y1, x2, y2, x_interval):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x_interval = x_interval


def interpolate_df_at_fixed_x_intervals(params: InterpolationParams):
    """
    Interpolate dataframes at fixed x intervals.
    """

    x_min = min(params.x1.min(), params.x2.min())
    x_max = max(params.x1.max(), params.x2.max())

    # Create a new set of x values at fixed intervals
    x_new = np.arange(x_min, x_max + params.x_interval, params.x_interval)
    x_new = pd.Series(x_new)

    # Create interpolated y values for each set of data at the new x values
    interpolation_func1 = interp1d(params.x1, params.y1, kind='linear', fill_value='extrapolate')
    interpolation_func2 = interp1d(params.x2, params.y2, kind='linear', fill_value='extrapolate')
    y1_new = interpolation_func1(x_new)
    y2_new = interpolation_func2(x_new)
    y_diff = y1_new - y2_new

    # Return a new dataframe with the new x values, and the two sets of y values
    df_interpolated = pd.DataFrame({
        params.x1.name + "_new": x_new,
        params.y1.name + "_new": y1_new,
        params.y2.name + "_new": y2_new,
        "y_diff": y_diff
    })

    return df_interpolated


def run(data1, data2, interval):
    """data1 and data2: DataFrames with the x column first and the y column second. Public entry point of this unit."""
    x1, y1 = data1.iloc[:, 0], data1.iloc[:, 1]
    x2, y2 = data2.iloc[:, 0], data2.iloc[:, 1]
    params = InterpolationParams(x1, y1, x2, y2, interval)
    return interpolate_df_at_fixed_x_intervals(params)
