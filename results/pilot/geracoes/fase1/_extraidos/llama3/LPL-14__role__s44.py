def simulate_bouncing_ball(state, time, physics=None):
    """Simulate the bouncing ball. Gravity affects the y coordinate only. When it its the floor on the y axis, it bounces back
    :param state: initial state (x0, y0, vx0, vy0)
    :param time: simulation time (steps, dt)
    :param physics: physical parameters (coefficient of restitution, gravity)
    :return: list of positions
    """
    x0, y0, vx0, vy0 = state
    steps, dt = time
    if physics is None:
        physics = Physics(coefficient_of_restitution=0.2, gravity=9.83)
    return simulate_bouncing_ball_core(state, time, physics)


def simulate_bouncing_ball_core(state, time, physics):
    x_positions = [state[0]]
    y_positions = [state[1]]
    vx = state[2]
    vy = state[3]
    for i in range(time[0]):
        x_positions.append(x_positions[-1] + vx * time[1])
        y_positions.append(y_positions[-1] + vy * time[1])
        if y_positions[-1] < 0:
            vy = -vy * physics.coefficient_of_restitution
            y_positions[-1] = 0
        else:
            y_positions[-1] = y_positions[-1] + vy * time[1]
            vy = vy - physics.gravity * time[1]
    return x_positions, y_positions


class Physics:
    def __init__(self, coefficient_of_restitution=0.2, gravity=9.83):
        self.coefficient_of_restitution = coefficient_of_restitution
        self.gravity = gravity

def executar(estado, tempo, fisica=None):
    """estado: (x0, y0, vx0, vy0). tempo: (passos, dt).

    fisica: (coeficiente de restituicao, gravidade); sem ela, valem os
    valores padrao da simulacao.
    """
    x0, y0, vx0, vy0 = estado
    steps, dt = tempo
    if fisica is None:
        return simulate_bouncing_ball((x0, y0, vx0, vy0), (steps, dt))
    coefficient_of_restitution, g = fisica
    return simulate_bouncing_ball((x0, y0, vx0, vy0), (steps, dt), Physics(coefficient_of_restitution, g))
