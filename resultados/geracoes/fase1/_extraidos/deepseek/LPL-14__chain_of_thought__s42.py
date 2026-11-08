class PhysicsParams:
    def __init__(self, coefficient_of_restitution=0.2, g=9.83):
        self.coefficient_of_restitution = coefficient_of_restitution
        self.g = g


def simulate_bouncing_ball(x0, y0, vx0, vy0, steps, dt, params: PhysicsParams):
    x_positions = [x0]
    y_positions = [y0]
    vx = vx0
    vy = vy0
    coefficient_of_restitution = params.coefficient_of_restitution
    g = params.g
    for i in range(steps):
        x_positions.append(x_positions[-1] + vx * dt)
        y_positions.append(y_positions[-1] + vy * dt)
        if y_positions[-1] < 0:
            vy = -vy * coefficient_of_restitution
            y_positions[-1] = 0
        else:
            y_positions[-1] = y_positions[-1] + vy * dt
            vy = vy - g * dt
    return x_positions, y_positions


def executar(estado, tempo, fisica=None):
    x0, y0, vx0, vy0 = estado
    steps, dt = tempo
    if fisica is None:
        params = PhysicsParams()
    else:
        coefficient_of_restitution, g = fisica
        params = PhysicsParams(coefficient_of_restitution, g)
    return simulate_bouncing_ball(x0, y0, vx0, vy0, steps, dt, params)
