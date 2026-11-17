"""Interpolation of two (x, y) series on the same set of equally spaced x.

Public entry point: run(data1, data2, interval). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


@dataclass
class InterpolationData:
    x: pd.Series
    y: pd.Series


@dataclass
class InterpolationParameters:
    interval: float


def interpolate_df_at_fixed_x_intervals(data1: InterpolationData, data2: InterpolationData, params: InterpolationParameters):
    """
    Interpolate dataframes at fixed x intervals.
    """

    x_min = min(data1.x.min(), data2.x.min())
    x_max = max(data1.x.max(), data2.x.max())

    # Create a new set of x values at fixed intervals
    x_new = np.arange(x_min, x_max + params.interval, params.interval)
    x_new = pd.Series(x_new)  # convert to a Pandas Series

    # Create interpolated y values for each set of data at the new x values
    interpolation_func1 = interp1d(data1.x, data1.y, kind='linear', fill_value='extrapolate')
    interpolation_func2 = interp1d(data2.x, data2.y, kind='linear', fill_value='extrapolate')
    y1_new = interpolation_func1(x_new)
    y2_new = interpolation_func2(x_new)
    y_diff = y1_new - y2_new  # better way than doing it later, below

    # Return a new dataframe with the new x values, and the two sets of y values
    df_interpolated = pd.DataFrame({
        data1.x.name + "_new": x_new,     # the new set of x-values; arbitrarily use `data1`'s name
        data1.y.name + "_new": y1_new,    # the new, interpolated y1 values
        data2.y.name + "_new": y2_new,    # the new, interpolated y2 values
        "y_diff": y_diff
    })

    return df_interpolated  # Contains x_new, y1_new, y2_new, and y_diff


def run(data1, data2, interval):
    """data1 and data2: DataFrames with the x column first and the y column second. Public entry point of this unit."""
    x1, y1 = data1.iloc[:, 0], data1.iloc[:, 1]
    x2, y2 = data2.iloc[:, 0], data2.iloc[:, 1]
    return interpolate_df_at_fixed_x_intervals(InterpolationData(x=x1, y=y1), InterpolationData(x=x2, y=y2), InterpolationParameters(interval=interval))
