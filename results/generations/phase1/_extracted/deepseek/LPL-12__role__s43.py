"""Interpolation of two  (x, y) series on the same set of equally spaced x.

Public entry point: run(data1, data2, interval). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


class ParameterObject:
    def __init__(self, x1, y1, x2, y2, x_interval):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x_interval = x_interval


def interpolate_df_at_fixed_x_intervals(parameter_object):
    """
    Interpolate dataframes at fixed x intervals.
    """

    x_min = min(parameter_object.x1.min(), parameter_object.x2.min())
    x_max = max(parameter_object.x1.max(), parameter_object.x2.max())

    # Create a new set of x values at fixed intervals
    x_new = np.arange(x_min, x_max + parameter_object.x_interval, parameter_object.x_interval)
    x_new = pd.Series(x_new)  # convert to a Pandas Series

    # Create interpolated y values for each set of data at the new x values
    interpolation_func1 = interp1d(parameter_object.x1, parameter_object.y1, kind='linear', fill_value='extrapolate')
    interpolation_func2 = interp1d(parameter_object.x2, parameter_object.y2, kind='linear', fill_value='extrapolate')
    y1_new = interpolation_func1(x_new)
    y2_new = interpolation_func2(x_new)
    y_diff = y1_new - y2_new  # better way than doing it later, below

    # Return a new dataframe with the new x values, and the two sets of y values
    df_interpolated = pd.DataFrame({
        parameter_object.x1.name + "_new": x_new,  # the new set of x-values; arbitrarily use `x1`'s name
        parameter_object.y1.name + "_new": y1_new,  # the new, interpolated y1 values
        parameter_object.y2.name + "_new": y2_new,  # the new, interpolated y2 values
        "y_diff": y_diff
    })

    return df_interpolated  # Contains x_new, y1_new, y2_new, and y_diff


def run(data1, data2, interval):
    """data1 and data2: DataFrames with the x column first and the y column second. Public entry point of this unit."""
    x1, y1 = data1.iloc[:, 0], data1.iloc[:, 1]
    x2, y2 = data2.iloc[:, 0], data2.iloc[:, 1]
    parameter_object = ParameterObject(x1, y1, x2, y2, interval)
    return interpolate_df_at_fixed_x_intervals(parameter_object)
