"""Simulation of a bouncing ball, step by step.

Public entry point: run(state, time, physics=None). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

class BounceParameters:
    def __init__(self, coefficient_of_restitution=0.2, g=9.83):
        self.coefficient_of_restitution = coefficient_of_restitution
        self.g = g

def simulate_bouncing_ball(state, time, physics: BounceParameters = None) -> list:
    """Simulate the bouncing ball. Gravity affects the y coordinate only. When it hits the floor on the y axis, it bounces back.
    :param state: (x0, y0, vx0, vy0)
    :param time: (steps, dt)
    :param physics: BounceParameters
    :return: list of positions
    """
    x0, y0, vx0, vy0 = state
    steps, dt = time
    coefficient_of_restitution = physics.coefficient_of_restitution if physics else 0.2
    g = physics.g if physics else 9.83

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


def run(state, time, physics=None):
    """state: (x0, y0, vx0, vy0). time: (steps, dt). Public entry point of this unit.

    physics: (coefficient of restitution, gravity); without it, the default
    values of the simulation apply.
    """
    x0, y0, vx0, vy0 = state
    steps, dt = time
    if physics is None:
        return simulate_bouncing_ball(state, time)
    return simulate_bouncing_ball(state, time, physics=BounceParameters(physics[0], physics[1]))
