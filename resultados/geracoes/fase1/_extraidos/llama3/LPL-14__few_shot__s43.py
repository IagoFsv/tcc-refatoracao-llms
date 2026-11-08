from dataclasses import dataclass, asdict

@dataclass
class Simulacao:
    estado: tuple
    tempo: tuple
    fisica: tuple | None = None

def simulate_bouncing_ball(simulacao: Simulacao) -> list:
    x0, y0, vx0, vy0 = simulacao.estado
    steps, dt = simulacao.tempo
    if simulacao.fisica is None:
        return simulate_bouncing_ball(x0, y0, vx0, vy0, steps, dt)
    coefficient_of_restitution, g = simulacao.fisica
    return simulate_bouncing_ball(x0, y0, vx0, vy0, steps, dt, coefficient_of_restitution, g)

def executar(simulacao: Simulacao):
    return simulate_bouncing_ball(simulacao)
