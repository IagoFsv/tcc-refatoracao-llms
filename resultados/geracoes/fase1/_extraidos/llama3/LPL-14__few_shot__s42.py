from dataclasses import dataclass, asdict

@dataclass
class Bola:
    x0: float
    y0: float
    vx0: float
    vy0: float
    steps: int
    dt: float
    coefficient_of_restitution: float = 0.2
    g: float = 9.83

def simulate_bouncing_ball(bola: Bola) -> tuple:
    x_positions = [bola.x0]
    y_positions = [bola.y0]
    vx = bola.vx0
    vy = bola.vy0
    for i in range(bola.steps):
        x_positions.append(x_positions[-1] + vx * bola.dt)
        y_positions.append(y_positions[-1] + vy * bola.dt)
        if y_positions[-1] < 0:
            vy = -vy * bola.coefficient_of_restitution
            y_positions[-1] = 0
        else:
            y_positions[-1] = y_positions[-1] + vy * bola.dt
            vy = vy - bola.g * bola.dt
    return x_positions, y_positions

def executar(estado, tempo, fisica=None):
    x0, y0, vx0, vy0 = estado
    steps, dt = tempo
    if fisica is None:
        return simulate_bouncing_ball(Bola(x0, y0, vx0, vy0, steps, dt))
    coefficient_of_restitution, g = fisica
    return simulate_bouncing_ball(Bola(x0, y0, vx0, vy0, steps, dt, coefficient_of_restitution, g))
