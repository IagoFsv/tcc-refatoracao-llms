"""Interpolation of two  (x, y) series on the same set of equally spaced x.

Public entry point: run(data1, data2, interval). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


class InterpolationData:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class InterpolationParams:
    def __init__(self, x_interval, x_min, x_max):
        self.x_interval = x_interval
        self.x_min = x_min
        self.x_max = x_max


def interpolate_df_at_fixed_x_intervals(data1: InterpolationData, data2: InterpolationData, params: InterpolationParams):
    """
    Interpolate dataframes at fixed x intervals.
    """

    # Create a new set of x values at fixed intervals
    x_new = np.arange(params.x_min, params.x_max + params.x_interval, params.x_interval)
    x_new = pd.Series(x_new)

    # Create interpolated y values for each set of data at the new x values
    interpolation_func1 = interp1d(data1.x, data1.y, kind='linear', fill_value='extrapolate')
    interpolation_func2 = interp1d(data2.x, data2.y, kind='linear', fill_value='extrapolate')
    y1_new = interpolation_func1(x_new)
    y2_new = interpolation_func2(x_new)
    y_diff = y1_new - y2_new

    # Return a new dataframe with the new x values, and the two sets of y values
    df_interpolated = pd.DataFrame({
        data1.x.name + "_new": x_new,
        data1.y.name + "_new": y1_new,
        data2.y.name + "_new": y2_new,
        "y_diff": y_diff
    })

    return df_interpolated


def run(data1, data2, interval):
    """data1 and data2: DataFrames with the x column first and the y column second. Public entry point of this unit."""
    x1, y1 = data1.iloc[:, 0], data1.iloc[:, 1]
    x2, y2 = data2.iloc[:, 0], data2.iloc[:, 1]

    x_min = min(x1.min(), x2.min())
    x_max = max(x1.max(), x2.max())

    data1 = InterpolationData(x1, y1)
    data2 = InterpolationData(x2, y2)
    params = InterpolationParams(interval, x_min, x_max)

    return interpolate_df_at_fixed_x_intervals(data1, data2, params)
