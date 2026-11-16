class SimulationParameters:
    def __init__(self, x0, y0, vx0, vy0, steps, dt, coefficient_of_restitution=0.2, g=9.83):
        self.x0 = x0
        self.y0 = y0
        self.vx0 = vx0
        self.vy0 = vy0
        self.steps = steps
        self.dt = dt
        self.coefficient_of_restitution = coefficient_of_restitution
        self.g = g

def simulate_bouncing_ball(parameters: SimulationParameters) -> list:
    x_positions = [parameters.x0]
    y_positions = [parameters.y0]
    vx = parameters.vx0
    vy = parameters.vy0
    for i in range(parameters.steps):
        x_positions.append(x_positions[-1] + vx * parameters.dt)
        y_positions.append(y_positions[-1] + vy * parameters.dt)
        if y_positions[-1] < 0:
            vy = -vy * parameters.coefficient_of_restitution
            y_positions[-1] = 0
        else:
            y_positions[-1] = y_positions[-1] + vy * parameters.dt
            vy = vy - parameters.g * parameters.dt
    return x_positions, y_positions

def executar(estado, tempo, fisica=None):
    x0, y0, vx0, vy0 = estado
    steps, dt = tempo
    parameters = SimulationParameters(x0, y0, vx0, vy0, steps, dt)
    if fisica is None:
        return simulate_bouncing_ball(parameters)
    coefficient_of_restitution, g = fisica
    parameters.coefficient_of_restitution = coefficient_of_restitution
    parameters.g = g
    return simulate_bouncing_ball(parameters)
