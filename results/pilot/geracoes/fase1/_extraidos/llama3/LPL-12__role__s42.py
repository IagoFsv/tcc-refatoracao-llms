import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

class DataInterpolator:
    def __init__(self, dados1, dados2, intervalo):
        self.dados1 = dados1
        self.dados2 = dados2
        self.intervalo = intervalo

    def interpolate_df_at_fixed_x_intervals(self):
        x_min = min(self.dados1.iloc[:, 0].min(), self.dados2.iloc[:, 0].min())
        x_max = max(self.dados1.iloc[:, 0].max(), self.dados2.iloc[:, 0].max())

        x_new = np.arange(x_min, x_max + self.intervalo, self.intervalo)
        x_new = pd.Series(x_new)

        interpolation_func1 = interp1d(self.dados1.iloc[:, 0], self.dados1.iloc[:, 1], kind='linear', fill_value='extrapolate')
        interpolation_func2 = interp1d(self.dados2.iloc[:, 0], self.dados2.iloc[:, 1], kind='linear', fill_value='extrapolate')
        y1_new = interpolation_func1(x_new)
        y2_new = interpolation_func2(x_new)
        y_diff = y1_new - y2_new

        df_interpolated = pd.DataFrame({
            "x": x_new,
            "y1": y1_new,
            "y2": y2_new,
            "y_diff": y_diff
        })

        return df_interpolated

def executar(dados1, dados2, intervalo):
    interpolator = DataInterpolator(dados1, dados2, intervalo)
    return interpolator.interpolate_df_at_fixed_x_intervals()
