from dataclasses import dataclass, asdict

@dataclass
class Dados:
    dados1: pd.DataFrame
    dados2: pd.DataFrame
    intervalo: float

def executar(dados: Dados):
    x1, y1 = dados.dados1.iloc[:, 0], dados.dados1.iloc[:, 1]
    x2, y2 = dados.dados2.iloc[:, 0], dados.dados2.iloc[:, 1]
    return interpolate_df_at_fixed_x_intervals(x1, y1, x2, y2, dados.intervalo)
