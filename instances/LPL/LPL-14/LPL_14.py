"""Simulation of a bouncing ball, step by step.

Public entry point: run(state, time, physics=None). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""


def simulate_bouncing_ball (x0, y0, vx0, vy0, steps, dt, coefficient_of_restitution = 0.2, g = 9.83) -> list:
    """>>>
    Simulate the bouncing ball. Gravity affects the y coordinate only. When it its the floor on the y axis, it bounces back
    :param x0: initial x position
    :param y0: initial y position
    :param vx0: initial x velocity
    :param vy0: initial y velocity
    :param steps: number of steps
    :param dt: time step
    :param g: gravity constant
    :param coefficient_of_restitution: coefficient of restitution of each bounce
    :return: list of positions
    """
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
        return simulate_bouncing_ball(x0, y0, vx0, vy0, steps, dt)
    coefficient_of_restitution, g = physics
    return simulate_bouncing_ball(x0, y0, vx0, vy0, steps, dt, coefficient_of_restitution, g)
