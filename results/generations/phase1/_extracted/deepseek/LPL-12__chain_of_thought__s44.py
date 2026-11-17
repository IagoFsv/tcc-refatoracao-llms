def run(data1, data2, interval):
    """data1 and data2: DataFrames with the x column first and the y column second. Public entry point of this unit."""
    x1, y1 = data1.iloc[:, 0], data1.iloc[:, 1]
    x2, y2 = data2.iloc[:, 0], data2.iloc[:, 1]
    data = Data(x1, y1, x2, y2, interval)
    return interpolate_df_at_fixed_x_intervals(data)
