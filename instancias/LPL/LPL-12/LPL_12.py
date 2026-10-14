"""Interpolacao de duas series (x, y) num mesmo conjunto de x igualmente espacados.

Ponto de entrada publico: executar(dados1, dados2, intervalo). Nao altere o
nome nem a assinatura dessa funcao; o restante do arquivo pode ser
reorganizado livremente.
"""

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


def interpolate_df_at_fixed_x_intervals(x1, y1, x2, y2, x_interval):
    """
    Interpolate dataframes at fixed x intervals.
    """

    x_min = min(x1.min(), x2.min())
    x_max = max(x1.max(), x2.max())

    # Create a new set of x values at fixed intervals
    # - The new x-values are produced as a floating point numpy `arange` array range of values.
    #   See: https://numpy.org/doc/stable/reference/generated/numpy.arange.html
    x_new = np.arange(x_min, x_max + x_interval, x_interval)  # <========= HOW TO CREATE A NEW NUMPY
                                                              # FLOATING POINT RANGE ARRAY (array
                                                              # range)
    x_new = pd.Series(x_new)  # convert to a Pandas Series

    # Create interpolated y values for each set of data at the new x values
    interpolation_func1 = interp1d(x1, y1, kind='linear', fill_value='extrapolate')
    interpolation_func2 = interp1d(x2, y2, kind='linear', fill_value='extrapolate')
    y1_new = interpolation_func1(x_new)
    y2_new = interpolation_func2(x_new)
    y_diff = y1_new - y2_new  # better way than doing it later, below

    # Return a new dataframe with the new x values, and the two sets of y values
    df_interpolated = pd.DataFrame({
        x1.name + "_new": x_new,     # the new set of x-values; arbitrarily use `x1`'s name
        y1.name + "_new": y1_new,    # the new, interpolated y1 values
        y2.name + "_new": y2_new,    # the new, interpolated y2 values
        # Better way than doing this later, below
        "y_diff": y_diff
    })

    # Do some math on the values; ex: calculate the difference between the two sets of y-values
    # - TODO/NB: if you know you need this calculation, it's cleaner to just do it *before* creating
    #   the `df_interpolated` dataframe above. See `interpolate_df_at_fixed_x_intervals_numpy()` in
    #   the method below, and instead just inject `"y_diff"` directly into `df_interpolated`
    #   DataFrame as you create it above.
    #
    # df_interpolated["y_diff"] = (
    #     df_interpolated[y1.name + "_new"] - df_interpolated[y2.name + "_new"])

    return df_interpolated  # Contains x_new, y1_new, y2_new, and y_diff


def executar(dados1, dados2, intervalo):
    """dados1 e dados2: DataFrames com a coluna de x primeiro e a de y depois."""
    x1, y1 = dados1.iloc[:, 0], dados1.iloc[:, 1]
    x2, y2 = dados2.iloc[:, 0], dados2.iloc[:, 1]
    return interpolate_df_at_fixed_x_intervals(x1, y1, x2, y2, intervalo)
