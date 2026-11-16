def simulate_bouncing_ball(state, time, physical_params=None):
    """Simulate the bouncing ball. Gravity affects the y coordinate only. When it hits the floor on the y axis, it bounces back
    :param state: initial state (x0, y0, vx0, vy0)
    :param time: time parameters (steps, dt)
    :param physical_params: physical parameters (coefficient_of_restitution, g); None for default values
    :return: list of positions
    """
    x0, y0, vx0, vy0 = state
    steps, dt = time
    if physical_params is None:
        physical_params = PhysicalParams(coefficient_of_restitution=0.2, g=9.83)
    return simulate_bouncing_ball_(state, time, physical_params)


class PhysicalParams:
    def __init__(self, coefficient_of_restitution=0.2, g=9.83):
        self.coefficient_of_restitution = coefficient_of_restitution
        self.g = g


def executar(estado, tempo):
    """estado: (x0, y0, vx0, vy0). tempo: (passos, dt).
    """
    x0, y0, vx0, vy0 = estado
    steps, dt = tempo
    return simulate_bouncing_ball((x0, y0, vx0, vy0), (steps, dt))
