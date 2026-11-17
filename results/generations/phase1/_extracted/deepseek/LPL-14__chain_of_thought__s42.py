class Physics:
    def __init__(self, coefficient_of_restitution=0.2, g=9.83):
        self.coefficient_of_restitution = coefficient_of_restitution
        self.g = g

class State:
    def __init__(self, x0, y0, vx0, vy0):
        self.x0 = x0
        self.y0 = y0
        self.vx0 = vx0
        self.vy0 = vy0

class Time:
    def __init__(self, steps, dt):
        self.steps = steps
        self.dt = dt

def simulate_bouncing_ball(state: State, time: Time, physics: Physics = None) -> list:
    """
    Simulate the bouncing ball. Gravity affects the y coordinate only. When it its the floor on the y axis, it bounces back
    :param state: initial state
    :param time: time parameters
    :param physics: physics parameters
    :return: list of positions
    """
    x0, y0, vx0, vy0 = state.x0, state.y0, state.vx0, state.vy0
    steps, dt = time.steps, time.dt
    if physics is None:
        physics = Physics()
    coefficient_of_restitution, g = physics.coefficient_of_restitution, physics.g

    x_positions = [x0]
    y_positions = [y0]
    vx = vx0
    vy = vy0
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


def run(state: State, time: Time, physics: Physics = None):
    """
    state: (x0, y0, vx0, vy0). time: (steps, dt). Public entry point of this unit.
    physics: (coefficient of restitution, gravity); without it, the default
    values of the simulation apply.
    """
    return simulate_bouncing_ball(state, time, physics)
