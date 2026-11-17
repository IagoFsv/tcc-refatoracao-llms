"""Simulation of a bouncing ball, step by step.

Public entry point: run(state, time, physics=None). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

class PhysicsParams:
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

def simulate_bouncing_ball(state: State, time: Time, physics: PhysicsParams = None) -> list:
    """>>>
    Simulate the bouncing ball. Gravity affects the y coordinate only. When it its the floor on the y axis, it bounces back
    :param state: initial state
    :param time: time step
    :param physics: physics parameters
    :return: list of positions
    """
    x_positions = [state.x0]
    y_positions = [state.y0]
    vx = state.vx0
    vy = state.vy0
    if physics is None:
        physics = PhysicsParams()
    for i in range(time.steps):
        x_positions.append(x_positions[-1] + vx * time.dt)
        y_positions.append(y_positions[-1] + vy * time.dt)
        if y_positions[-1] < 0:
            vy = -vy * physics.coefficient_of_restitution
            y_positions[-1] = 0
        else:
            y_positions[-1] = y_positions[-1] + vy * time.dt
            vy = vy - physics.g * time.dt
    return x_positions, y_positions


def run(state: State, time: Time, physics: PhysicsParams = None):
    """state: (x0, y0, vx0, vy0). time: (steps, dt). Public entry point of this unit.

    physics: (coefficient of restitution, gravity); without it, the default
    values of the simulation apply.
    """
    return simulate_bouncing_ball(state, time, physics)
