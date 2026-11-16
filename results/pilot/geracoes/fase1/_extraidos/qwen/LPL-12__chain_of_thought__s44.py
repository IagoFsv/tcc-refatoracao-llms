import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

class InterpolationData:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def interpolate_df_at_fixed_x_intervals(data1, data2, x_interval):
    """
    Interpolate dataframes at fixed x intervals.
    """

    x_min = min(data1.x.min(), data2.x.min())
    x_max = max(data1.x.max(), data2.x.max())

    # Create a new set of x values at fixed intervals
    x_new = np.arange(x_min, x_max + x_interval, x_interval)
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


def executar(dados1, dados2, intervalo):
    """dados1 e dados2: DataFrames com a coluna de x primeiro e a de y depois."""
    data1_obj = InterpolationData(dados1.iloc[:, 0], dados1.iloc[:, 1])
    data2_obj = InterpolationData(dados2.iloc[:, 0], dados2.iloc[:, 1])
    return interpolate_df_at_fixed_x_intervals(data1_obj, data2_obj, intervalo)
