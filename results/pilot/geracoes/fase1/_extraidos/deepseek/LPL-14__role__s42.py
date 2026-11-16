class Params:
    def __init__(self, coefficient_of_restitution, g):
        self.coefficient_of_restitution = coefficient_of_restitution
        self.g = g

def simulate_bouncing_ball(x0, y0, vx0, vy0, steps, dt, params: Params):
    x_positions = [x0]
    y_positions = [y0]
    vx = vx0
    vy = vy0
    for i in range(steps):
        x_positions.append(x_positions[-1] + vx * dt)
        y_positions.append(y_positions[-1] + vy * dt)
        if y_positions[-1] < 0:
            vy = -vy * params.coefficient_of_restitution
            y_positions[-1] = 0
        else:
            y_positions[-1] = y_positions[-1] + vy * dt
            vy = vy - params.g * dt
    return x_positions, y_positions


def executar(estado, tempo, params: Params = None):
    x0, y0, vx0, vy0 = estado
    steps, dt = tempo
    if params is None:
        params = Params(0.2, 9.83)
    return simulate_bouncing_ball(x0, y0, vx0, vy0, steps, dt, params)
