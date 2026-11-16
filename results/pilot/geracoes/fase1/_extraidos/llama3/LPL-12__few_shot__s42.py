from dataclasses import dataclass, asdict

@dataclass
class Dados:
    x: pd.Series
    y: pd.Series

def interpolate_df_at_fixed_x_intervals(dados: Dados, intervalo: float):
    x_min = min(dados.x.min(), dados.x.max())
    x_max = max(dados.x.min(), dados.x.max())

    x_new = np.arange(x_min, x_max + intervalo, intervalo)
    x_new = pd.Series(x_new)

    interpolation_func1 = interp1d(dados.x, dados.y, kind='linear', fill_value='extrapolate')
    y1_new = interpolation_func1(x_new)
    y_diff = y1_new

    df_interpolated = pd.DataFrame({
        "x_new": x_new,
        "y1_new": y1_new,
        "y_diff": y_diff
    })

    return df_interpolated

def executar(dados1: Dados, dados2: Dados, intervalo: float):
    return interpolate_df_at_fixed_x_intervals(dados1, intervalo), interpolate_df_at_fixed_x_intervals(dados2, intervalo)
