from dataclasses import dataclass, asdict

@dataclass
class Estado:
    x0: float
    y0: float
    vx0: float
    vy0: float

@dataclass
class Tempo:
    steps: int
    dt: float

@dataclass
class Fisica:
    coefficient_of_restitution: float = 0.2
    g: float = 9.83

def simulate_bouncing_ball(estado: Estado, tempo: Tempo, fisica: Fisica = None) -> list:
    x_positions = [estado.x0]
    y_positions = [estado.y0]
    vx = estado.vx0
    vy = estado.vy0
    coefficient_of_restitution = fisica.coefficient_of_restitution if fisica else 0.2
    g = fisica.g if fisica else 9.83
    for i in range(tempo.steps):
        x_positions.append(x_positions[-1] + vx * tempo.dt)
        y_positions.append(y_positions[-1] + vy * tempo.dt)
        if y_positions[-1] < 0:
            vy = -vy * coefficient_of_restitution
            y_positions[-1] = 0
        else:
            y_positions[-1] = y_positions[-1] + vy * tempo.dt
            vy = vy - g * tempo.dt
    return x_positions, y_positions

def executar(estado: Estado, tempo: Tempo, fisica: Fisica = None):
    return simulate_bouncing_ball(estado, tempo, fisica)
