"""Simulation of a bouncing ball, step by step.

Public entry point: run(state, time, physics=None). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

class PhysicsParams:
    def __init__(self, coefficient_of_restitution=0.2, g=9.83):
        self.coefficient_of_restitution = coefficient_of_restitution
        self.g = g


def simulate_bouncing_ball(initial_state, time_params, physics_params=PhysicsParams()) -> list:
    """Simulate the bouncing ball. Gravity affects the y coordinate only. When it hits the floor on the y axis, it bounces back
    :param initial_state: Initial state of the ball (x0, y0, vx0, vy0)
    :param time_params: Time parameters (steps, dt)
    :param physics_params: Physics parameters (coefficient_of_restitution, g)
    :return: list of positions
    """
    x0, y0, vx0, vy0 = initial_state
    steps, dt = time_params
    coefficient_of_restitution = physics_params.coefficient_of_restitution
    g = physics_params.g

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
    initial_state = state
    time_params = time
    physics_params = PhysicsParams() if physics is None else PhysicsParams(*physics)
    return simulate_bouncing_ball(initial_state, time_params, physics_params)
