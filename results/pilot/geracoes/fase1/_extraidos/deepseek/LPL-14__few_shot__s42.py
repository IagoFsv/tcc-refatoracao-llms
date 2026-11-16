"""Simulacao de uma bola quicando, passo a passo.

Ponto de entrada publico: executar(estado, tempo, fisica=None). Nao altere o
nome nem a assinatura dessa funcao; o restante do arquivo pode ser
reorganizado livremente.
"""

from dataclasses import dataclass, asdict

@dataclass
class Fisica:
    coeficiente_de_restituicao: float = 0.2
    gravidade: float = 9.83

def simulate_bouncing_ball(x0, y0, vx0, vy0, steps, dt, fisica: Fisica) -> list:
    """>>>
    Simulate the bouncing ball. Gravity affects the y coordinate only. When it its the floor on the y axis, it bounces back
    :param x0: initial x position
    :param y0: initial y position
    :param vx0: initial x velocity
    :param vy0: initial y velocity
    :param steps: number of steps
    :param dt: time step
    :param fisica: physics parameters
    :return: list of positions
    """
    x_positions = [x0]
    y_positions = [y0]
    vx = vx0
    vy = vy0
    for i in range(steps):
        x_positions.append(x_positions[-1] + vx * dt)
        y_positions.append(y_positions[-1] + vy * dt)
        if y_positions[-1] < 0:
            vy = -vy * fisica.coeficiente_de_restituicao
            y_positions[-1] = 0
        else:
            y_positions[-1] = y_positions[-1] + vy * dt
            vy = vy - fisica.gravidade * dt
    return x_positions, y_positions


def executar(estado, tempo, fisica=None):
    """estado:  (x0, y0, vx0, vy0). tempo:  (passos, dt).

    fisica:  (coeficiente_de_restituicao, gravidade); sem ela, valem os
    valores padrao da simulacao.
    """
    x0, y0, vx0, vy0 = estado
    steps, dt = tempo
    if fisica is None:
        return simulate_bouncing_ball(x0, y0, vx0, vy0, steps, dt, Fisica())
    coeficiente_de_restituicao, g = fisica
    return simulate_bouncing_ball(x0, y0, vx0, vy0, steps, dt, Fisica(coeficiente_de_restituicao, g))
