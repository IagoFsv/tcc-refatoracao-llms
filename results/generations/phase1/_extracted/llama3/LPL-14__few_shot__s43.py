from dataclasses import dataclass, asdict

@dataclass
class State:
    x0: float
    y0: float
    vx0: float
    vy0: float

@dataclass
class Time:
    steps: int
    dt: float

@dataclass
class Physics:
    coefficient_of_restitution: float
    gravity: float

def simulate_bouncing_ball(state: State, time: Time, physics: Physics) -> tuple:
    x_positions = [state.x0]
    y_positions = [state.y0]
    vx = state.vx0
    vy = state.vy0
    for i in range(time.steps):
        x_positions.append(x_positions[-1] + vx * time.dt)
        y_positions.append(y_positions[-1] + vy * time.dt)
        if y_positions[-1] < 0:
            vy = -vy * physics.coefficient_of_restitution
            y_positions[-1] = 0
        else:
            y_positions[-1] = y_positions[-1] + vy * time.dt
            vy = vy - physics.gravity * time.dt
    return x_positions, y_positions

def run(state: State, time: Time, physics: Physics = None):
    if physics is None:
        return simulate_bouncing_ball(state, time, physics)
    return simulate_bouncing_ball(state, time, physics)
