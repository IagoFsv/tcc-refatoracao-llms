"""Simulation of a bouncing ball, step by step.

Public entry point: run(state, time, physics=None). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

from dataclasses import dataclass, asdict

@dataclass
class BallState:
    x0: float
    y0: float
    vx0: float
    vy0: float

@dataclass
class SimulationTime:
    steps: int
    dt: float

@dataclass
class PhysicsParameters:
    coefficient_of_restitution: float = 0.2
    g: float = 9.83

def simulate_bouncing_ball(state: BallState, time: SimulationTime, physics: PhysicsParameters = PhysicsParameters()) -> tuple:
    """Simulate the bouncing ball. Gravity affects the y coordinate only. When it hits the floor on the y axis, it bounces back."""
    x_positions = [state.x0]
    y_positions = [state.y0]
    vx = state.vx0
    vy = state.vy0
    coefficient_of_restitution = physics.coefficient_of_restitution
    g = physics.g
    for _ in range(time.steps):
        x_positions.append(x_positions[-1] + vx * time.dt)
        y_positions.append(y_positions[-1] + vy * time.dt)
        if y_positions[-1] < 0:
            vy = -vy * coefficient_of_restitution
            y_positions[-1] = 0
        else:
            vy = vy - g * time.dt
    return x_positions, y_positions


def run(state: tuple, time: tuple, physics: tuple = None) -> tuple:
    """state: (x0, y0, vx0, vy0). time: (steps, dt). Public entry point of this unit.

    physics: (coefficient of restitution, gravity); without it, the default
    values of the simulation apply.
    """
    ball_state = BallState(*state)
    simulation_time = SimulationTime(*time)
    if physics is None:
        physics_params = PhysicsParameters()
    else:
        physics_params = PhysicsParameters(*physics)
    return simulate_bouncing_ball(ball_state, simulation_time, physics_params)
