from dataclasses import dataclass, asdict

@dataclass
class BouncingBallState:
    x0: float
    y0: float
    vx0: float
    vy0: float

@dataclass
class BouncingBallPhysics:
    coefficient_of_restitution: float = 0.2
    g: float = 9.83

def simulate_bouncing_ball(state: BouncingBallState, steps: int, dt: float, physics: BouncingBallPhysics) -> list:
    x_positions = [state.x0]
    y_positions = [state.y0]
    vx = state.vx0
    vy = state.vy0
    for _ in range(steps):
        x_positions.append(x_positions[-1] + vx * dt)
        y_positions.append(y_positions[-1] + vy * dt)
        if y_positions[-1] < 0:
            vy = -vy * physics.coefficient_of_restitution
            y_positions[-1] = 0
        else:
            vy = vy - physics.g * dt
    return x_positions, y_positions

def executar(estado: BouncingBallState, tempo: tuple, fisica: BouncingBallPhysics = None) -> list:
    steps, dt = tempo
    if fisica is None:
        return simulate_bouncing_ball(estado, steps, dt, BouncingBallPhysics())
    return simulate_bouncing_ball(estado, steps, dt, fisica)
