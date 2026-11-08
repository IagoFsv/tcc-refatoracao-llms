import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

class InterpolationData:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

def interpolate_df_at_fixed_x_intervals(interpolation_data, x_interval):
    x_min = min(interpolation_data.x1.min(), interpolation_data.x2.min())
    x_max = max(interpolation_data.x1.max(), interpolation_data.x2.max())

    x_new = np.arange(x_min, x_max + x_interval, x_interval)
    x_new = pd.Series(x_new)

    interpolation_func1 = interp1d(interpolation_data.x1, interpolation_data.y1, kind='linear', fill_value='extrapolate')
    interpolation_func2 = interp1d(interpolation_data.x2, interpolation_data.y2, kind='linear', fill_value='extrapolate')
    y1_new = interpolation_func1(x_new)
    y2_new = interpolation_func2(x_new)
    y_diff = y1_new - y2_new

    df_interpolated = pd.DataFrame({
        'x_new': x_new,  # the new set of x-values; arbitrarily use `x1`'s name
        'y1_new': y1_new,  # the new, interpolated y1 values
        'y2_new': y2_new,  # the new, interpolated y2 values
        'y_diff': y_diff
    })

    return df_interpolated

def executar(dados1, dados2, intervalo):
    x1, y1 = dados1.iloc[:, 0], dados1.iloc[:, 1]
    x2, y2 = dados2.iloc[:, 0], dados2.iloc[:, 1]
    interpolation_data = InterpolationData(x1, y1, x2, y2)
    return interpolate_df_at_fixed_x_intervals(interpolation_data, intervalo)
