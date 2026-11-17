"""Interpolation of two (x, y) series on the same set of equally spaced x.

Public entry point: run(data1, data2, interval). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


class Data:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def interpolate_df_at_fixed_x_intervals(data1, data2, interval):
    x_min = min(data1.x.min(), data2.x.min())
    x_max = max(data1.x.max(), data2.x.max())

    x_new = pd.Series(np.arange(x_min, x_max + interval, interval))
    interpolation_func1 = interp1d(data1.x, data1.y, kind='linear', fill_value='extrapolate')
    interpolation_func2 = interp1d(data2.x, data2.y, kind='linear', fill_value='extrapolate')
    y1_new = interpolation_func1(x_new)
    y2_new = interpolation_func2(x_new)
    y_diff = y1_new - y2_new

    df_interpolated = pd.DataFrame({
        data1.x.name + "_new": x_new,
        "y1_new": y1_new,
        "y2_new": y2_new,
        "y_diff": y_diff
    })

    return df_interpolated


def run(data1, data2, interval):
    return interpolate_df_at_fixed_x_intervals(Data(data1.x, data1.y), Data(data2.x, data2.y), interval)
