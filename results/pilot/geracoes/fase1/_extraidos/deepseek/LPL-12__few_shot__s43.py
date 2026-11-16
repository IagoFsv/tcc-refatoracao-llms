from dataclasses import dataclass, asdict

@dataclass
class Dados:
    dados1: pd.DataFrame
    dados2: pd.DataFrame
    intervalo: float

def interpolate_df_at_fixed_x_intervals(x1, y1, x2, y2, x_interval):
    """
    Interpolate dataframes at fixed x intervals.
    """

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


def executar(dados: Dados):
    x1, y1 = dados.dados1.iloc[:, 0], dados.dados1.iloc[:, 1]
    x2, y2 = dados.dados2.iloc[:, 0], dados.dados2.iloc[:, 1]
    return interpolate_df_at_fixed_x_intervals(x1, y1, x2, y2, dados.intervalo)
