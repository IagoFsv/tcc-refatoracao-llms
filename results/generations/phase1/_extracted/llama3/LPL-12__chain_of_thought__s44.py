"""Interpolation of two (x, y) series on the same set of equally spaced x.

Public entry point: run(data1, data2, interval). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


class DataInterval:
    def __init__(self, data1, data2, interval):
        self.data1 = data1
        self.data2 = data2
        self.interval = interval


def interpolate_df_at_fixed_x_intervals(data_interval):
    """
    Interpolate dataframes at fixed x intervals.
    """

    x_min = min(data_interval.data1.iloc[:, 0].min(), data_interval.data2.iloc[:, 0].min())
    x_max = max(data_interval.data1.iloc[:, 0].max(), data_interval.data2.iloc[:, 0].max())

    # Create a new set of x values at fixed intervals
    # - The new x-values are produced as a floating point numpy `arange` array range of values.
    #   See: https://numpy.org/doc/stable/reference/generated/numpy.arange.html
    x_new = np.arange(x_min, x_max + data_interval.interval, data_interval.interval)  # <========= HOW TO CREATE A NEW NUMPY
                                                                                     # FLOATING POINT RANGE ARRAY (array
                                                                                     # range)
    x_new = pd.Series(x_new)  # convert to a Pandas Series

    # Create interpolated y values for each set of data at the new x values
    interpolation_func1 = interp1d(data_interval.data1.iloc[:, 0], data_interval.data1.iloc[:, 1], kind='linear', fill_value='extrapolate')
    interpolation_func2 = interp1d(data_interval.data2.iloc[:, 0], data_interval.data2.iloc[:, 1], kind='linear', fill_value='extrapolate')
    y1_new = interpolation_func1(x_new)
    y2_new = interpolation_func2(x_new)
    y_diff = y1_new - y2_new  # better way than doing it later, below

    # Return a new dataframe with the new x values, and the two sets of y values
    df_interpolated = pd.DataFrame({
        data_interval.data1.iloc[:, 0].name + "_new": x_new,     # the new set of x-values; arbitrarily use `x1`'s name
        data_interval.data1.iloc[:, 1].name + "_new": y1_new,    # the new, interpolated y1 values
        data_interval.data2.iloc[:, 1].name + "_new": y2_new,    # the new, interpolated y2 values
        "y_diff": y_diff
    })

    # Do some math on the values; ex: calculate the difference between the two sets of y-values
    # - TODO/NB: if you know you need this calculation, it's cleaner to just do it *before* creating
    #   the `df_interpolated` dataframe above. See `interpolate_df_at_fixed_x_intervals_numpy()` in
    #   the method below, and instead just inject `"y_diff"` directly into `df_interpolated`
    #   DataFrame as you create it above.
    #
    # df_interpolated["y_diff"] = (
    #     df_interpolated[data_interval.data1.iloc[:, 1].name + "_new"] - df_interpolated[data_interval.data2.iloc[:, 1].name + "_new"])

    return df_interpolated  # Contains x_new, y1_new, y2_new, and y_diff


def run(data1, data2, interval):
    """data1 and data2: DataFrames with the x column first and the y column second. Public entry point of this unit."""
    data_interval = DataInterval(data1, data2, interval)
    return interpolate_df_at_fixed_x_intervals(data_interval)
