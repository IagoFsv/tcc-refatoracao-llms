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
    x1, y1 = parameter_object.x1, parameter_object.y1
    x2, y2 = parameter_object.x2, parameter_object.y2
    x_interval = parameter_object.x_interval

    x_min = min(x1.min(), x2.min())
    x_max = max(x1.max(), x2.max())

    x_new = np.arange(x_min, x_max + x_interval, x_interval)
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

def executar(dados1, dados2, intervalo):
    """dados1 e dados2: DataFrames com a coluna de x primeiro e a de y depois."""
    x1, y1 = dados1.iloc[:, 0], dados1.iloc[:, 1]
    x2, y2 = dados2.iloc[:, 0], dados2.iloc[:, 1]
    parameter_object = ParameterObject(x1, y1, x2, y2, intervalo)
    return interpolate_df_at_fixed_x_intervals(parameter_object)
