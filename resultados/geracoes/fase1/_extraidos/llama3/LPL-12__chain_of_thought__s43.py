class InterpolationData:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def interpolate(self, x_interval):
        x_min = min(self.x1.min(), self.x2.min())
        x_max = max(self.x1.max(), self.x2.max())

        x_new = np.arange(x_min, x_max + x_interval, x_interval)
        x_new = pd.Series(x_new)

        interpolation_func1 = interp1d(self.x1, self.y1, kind='linear', fill_value='extrapolate')
        interpolation_func2 = interp1d(self.x2, self.y2, kind='linear', fill_value='extrapolate')
        y1_new = interpolation_func1(x_new)
        y2_new = interpolation_func2(x_new)
        y_diff = y1_new - y2_new

        df_interpolated = pd.DataFrame({
            self.x1.name + "_new": x_new,
            self.y1.name + "_new": y1_new,
            self.y2.name + "_new": y2_new,
            "y_diff": y_diff
        })

        return df_interpolated

def executar(dados1, dados2, intervalo):
    x1, y1 = dados1.iloc[:, 0], dados1.iloc[:, 1]
    x2, y2 = dados2.iloc[:, 0], dados2.iloc[:, 1]
    interpolation_data = InterpolationData(x1, y1, x2, y2)
    return interpolation_data.interpolate(intervalo)
