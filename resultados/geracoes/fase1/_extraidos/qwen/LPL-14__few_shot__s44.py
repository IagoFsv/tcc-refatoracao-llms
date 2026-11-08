from dataclasses import dataclass, asdict

@dataclass
class BouncingBallParameters:
    x0: float
    y0: float
    vx0: float
    vy0: float
    steps: int
    dt: float
    coefficient_of_restitution: float = 0.2
    g: float = 9.83

def simulate_bouncing_ball(params: BouncingBallParameters) -> list:
    x_positions = [params.x0]
    y_positions = [params.y0]
    vx = params.vx0
    vy = params.vy0
    for i in range(params.steps):
        x_positions.append(x_positions[-1] + vx * params.dt)
        y_positions.append(y_positions[-1] + vy * params.dt)
        if y_positions[-1] < 0:
            vy = -vy * params.coefficient_of_restitution
            y_positions[-1] = 0
        else:
            y_positions[-1] = y_positions[-1] + vy * params.dt
            vy = vy - params.g * params.dt
    return x_positions, y_positions

def executar(estado, tempo, fisica=None):
    x0, y0, vx0, vy0 = estado
    steps, dt = tempo
    params = BouncingBallParameters(x0, y0, vx0, vy0, steps, dt)
    if fisica is not None:
        params.coefficient_of_restitution, params.g = fisica
    return simulate_bouncing_ball(params)
