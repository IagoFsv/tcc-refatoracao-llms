from dataclasses import dataclass, asdict

@dataclass
class Physics:
    coefficient_of_restitution: float = 0.2
    g: float = 9.83

@dataclass
class BouncingBall:
    x0: float
    y0: float
    vx0: float
    vy0: float
    steps: int
    dt: float

def simulate_bouncing_ball(ball: BouncingBall, physics: Physics) -> list:
    x_positions = [ball.x0]
    y_positions = [ball.y0]
    vx = ball.vx0
    vy = ball.vy0
    for i in range(ball.steps):
        x_positions.append(x_positions[-1] + vx * ball.dt)
        y_positions.append(y_positions[-1] + vy * ball.dt)
        if y_positions[-1] < 0:
            vy = -vy * physics.coefficient_of_restitution
            y_positions[-1] = 0
        else:
            y_positions[-1] = y_positions[-1] + vy * ball.dt
            vy = vy - physics.g * ball.dt
    return x_positions, y_positions

def executar(estado, tempo, fisica=None):
    x0, y0, vx0, vy0 = estado
    steps, dt = tempo
    if fisica is None:
        return simulate_bouncing_ball(BouncingBall(x0, y0, vx0, vy0, steps, dt), Physics())
    coefficient_of_restitution, g = fisica
    return simulate_bouncing_ball(BouncingBall(x0, y0, vx0, vy0, steps, dt), Physics(coefficient_of_restitution, g))
