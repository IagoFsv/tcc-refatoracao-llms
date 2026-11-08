def executar(dados1, dados2, intervalo):
    parameters = Parameters(dados1.iloc[:, 0], dados1.iloc[:, 1], dados2.iloc[:, 0], dados2.iloc[:, 1], intervalo)
    return interpolate_df_at_fixed_x_intervals(parameters)
