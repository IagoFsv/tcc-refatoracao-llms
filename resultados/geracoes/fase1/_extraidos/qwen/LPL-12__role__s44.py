import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

class InterpolationParameters:
    def __init__(self, x1, y1, x2, y2, x_interval):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x_interval = x_interval

def interpolate_df_at_fixed_x_intervals(params):
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

def executar(dados1, dados2, intervalo):
    """dados1 e dados2: DataFrames com a coluna de x primeiro e a de y depois."""
    x1, y1 = dados1.iloc[:, 0], dados1.iloc[:, 1]
    x2, y2 = dados2.iloc[:, 0], dados2.iloc[:, 1]
    params = InterpolationParameters(x1, y1, x2, y2, intervalo)
    return interpolate_df_at_fixed_x_intervals(params)
