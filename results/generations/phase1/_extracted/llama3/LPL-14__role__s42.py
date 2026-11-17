"""Simulation of a bouncing ball, step by step.

Public entry point: run(state, time, physics=None). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""


class SimulationConfig:
    def __init__(self, x0, y0, vx0, vy0, steps, dt, coefficient_of_restitution=0.2, g=9.83):
        self.x0 = x0
        self.y0 = y0
        self.vx0 = vx0
        self.vy0 = vy0
        self.steps = steps
        self.dt = dt
        self.coefficient_of_restitution = coefficient_of_restitution
        self.g = g


def simulate_bouncing_ball(config: SimulationConfig) -> tuple:
    """>>
    Simulate the bouncing ball. Gravity affects the y coordinate only. When it hits the floor on the y axis, it bounces back
    :param config: simulation configuration
    :return: list of positions
    """
    x_positions = [config.x0]
    y_positions = [config.y0]
    vx = config.vx0
    vy = config.vy0
    for i in range(config.steps):
        x_positions.append(x_positions[-1] + vx * config.dt)
        y_positions.append(y_positions[-1] + vy * config.dt)
        if y_positions[-1] < 0:
            vy = -vy * config.coefficient_of_restitution
            y_positions[-1] = 0
        else:
            y_positions[-1] = y_positions[-1] + vy * config.dt
            vy = vy - config.g * config.dt
    return x_positions, y_positions


def run(state, time, physics=None):
    """state: (x0, y0, vx0, vy0). time: (steps, dt). Public entry point of this unit.

    physics: (coefficient of restitution, gravity); without it, the default
    values of the simulation apply.
    """
    x0, y0, vx0, vy0 = state
    steps, dt = time
    config = SimulationConfig(x0, y0, vx0, vy0, steps, dt)
    if physics is None:
        return simulate_bouncing_ball(config)
    coefficient_of_restitution, g = physics
    config.coefficient_of_restitution = coefficient_of_restitution
    config.g = g
    return simulate_bouncing_ball(config)
