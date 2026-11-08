class Parameters:
    def __init__(self, x0, y0, vx0, vy0, steps, dt, coefficient_of_restitution=0.2, g=9.83):
        self.x0 = x0
        self.y0 = y0
        self.vx0 = vx0
        self.vy0 = vy0
        self.steps = steps
        self.dt = dt
        self.coefficient_of_restitution = coefficient_of_restitution
        self.g = g


def simulate_bouncing_ball(params: Parameters) -> list:
    """>>>
    Simulate the bouncing ball. Gravity affects the y coordinate only. When it its the floor on the y axis, it bounces back
    :param params: Parameters object
    :return: list of positions
    """
    x_positions = [params.x0]
    y_positions = [params.y0]
    vx = params.vx0
    vy = params.vy0
    for i in range(params.steps):
        x_positions.append(x_positions[-1] + vx * params.dt)
        y_positions.append(y_positions[-1] + vy * params.dt)
        if y_positions[-1] < 0:
            vy = -vy * params.coefficient_of_restitution
            y_positions[-1] = 0
        else:
            y_positions[-1] = y_positions[-1] + vy * params.dt
            vy = vy - params.g * params.dt
    return x_positions, y_positions


def executar(estado, tempo, fisica=None):
    """estado: (x0, y0, vx0, vy0). tempo: (passos, dt).
    fisica: (coeficiente de restituicao, gravidade); sem ela, valem os
    valores padrao da simulacao.
    """
    x0, y0, vx0, vy0 = estado
    steps, dt = tempo
    if fisica is None:
        params = Parameters(x0, y0, vx0, vy0, steps, dt)
    else:
        coefficient_of_restitution, g = fisica
        params = Parameters(x0, y0, vx0, vy0, steps, dt, coefficient_of_restitution, g)
    return simulate_bouncing_ball(params)
