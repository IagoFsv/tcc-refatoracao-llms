from dataclasses import dataclass, asdict

@dataclass
class BouncingBallState:
    x0: float
    y0: float
    vx0: float
    vy0: float

@dataclass
class SimulationParameters:
    steps: int
    dt: float
    coefficient_of_restitution: float = 0.2
    g: float = 9.83

def simulate_bouncing_ball(state: BouncingBallState, parameters: SimulationParameters) -> tuple:
    x_positions = [state.x0]
    y_positions = [state.y0]
    vx = state.vx0
    vy = state.vy0
    for i in range(parameters.steps):
        x_positions.append(x_positions[-1] + vx * parameters.dt)
        y_positions.append(y_positions[-1] + vy * parameters.dt)
        if y_positions[-1] < 0:
            vy = -vy * parameters.coefficient_of_restitution
            y_positions[-1] = 0
        else:
            y_positions[-1] = y_positions[-1] + vy * parameters.dt
            vy = vy - parameters.g * parameters.dt
    return x_positions, y_positions

def run(state: BouncingBallState, time: tuple, physics: tuple = None) -> tuple:
    if physics is None:
        return simulate_bouncing_ball(state, time)
    coefficient_of_restitution, g = physics
    return simulate_bouncing_ball(state, SimulationParameters(*time, coefficient_of_restitution, g))
