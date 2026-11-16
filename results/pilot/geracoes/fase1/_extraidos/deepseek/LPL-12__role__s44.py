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

def interpolate_df_at_fixed_x_intervals(parameters):
    x_min = min(parameters.x1.min(), parameters.x2.min())
    x_max = max(parameters.x1.max(), parameters.x2.max())

    x_new = np.arange(x_min, x_max + parameters.x_interval, parameters.x_interval)
    x_new = pd.Series(x_new)

    interpolation_func1 = interp1d(parameters.x1, parameters.y1, kind='linear', fill_value='extrapolate')
    interpolation_func2 = interp1d(parameters.x2, parameters.y2, kind='linear', fill_value='extrapolate')
    y1_new = interpolation_func1(x_new)
    y2_new = interpolation_func2(x_new)
    y_diff = y1_new - y2_new

    df_interpolated = pd.DataFrame({
        parameters.x1.name + "_new": x_new,
        parameters.y1.name + "_new": y1_new,
        parameters.y2.name + "_new": y2_new,
        "y_diff": y_diff
    })

    return df_interpolated


def executar(dados1, dados2, intervalo):
    x1, y1 = dados1.iloc[:, 0], dados1.iloc[:, 1]
    x2, y2 = dados2.iloc[:, 0], dados2.iloc[:, 1]
    parameters = ParameterObject(x1, y1, x2, y2, intervalo)
    return interpolate_df_at_fixed_x_intervals(parameters)
