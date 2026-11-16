from dataclasses import dataclass, asdict
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

@dataclass
class Dados:
    x1: pd.Series
    y1: pd.Series
    x2: pd.Series
    y2: pd.Series

def interpolate_df_at_fixed_x_intervals(dados: Dados, intervalo: float):
    x_min = min(dados.x1.min(), dados.x2.min())
    x_max = max(dados.x1.max(), dados.x2.max())

    x_new = np.arange(x_min, x_max + intervalo, intervalo)
    x_new = pd.Series(x_new)

    interpolation_func1 = interp1d(dados.x1, dados.y1, kind='linear', fill_value='extrapolate')
    interpolation_func2 = interp1d(dados.x2, dados.y2, kind='linear', fill_value='extrapolate')
    y1_new = interpolation_func1(x_new)
    y2_new = interpolation_func2(x_new)
    y_diff = y1_new - y2_new

    df_interpolated = pd.DataFrame({
        'x_new': x_new,
        'y1_new': y1_new,
        'y2_new': y2_new,
        'y_diff': y_diff
    })

    return df_interpolated

def executar(dados1, dados2, intervalo):
    return interpolate_df_at_fixed_x_intervals(Dados(x1=dados1.iloc[:, 0], y1=dados1.iloc[:, 1], x2=dados2.iloc[:, 0], y2=dados2.iloc[:, 1]), intervalo)
