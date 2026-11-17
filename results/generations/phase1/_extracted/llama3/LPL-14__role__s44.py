"""Simulation of a bouncing ball, step by step.

Public entry point: run(state, time, physics=None). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""


class BouncingBallSimulation:
    def __init__(self, initial_state, time_step, physics=None):
        self.initial_state = initial_state
        self.time_step = time_step
        self.physics = physics

    def simulate(self) -> list:
        x0, y0, vx0, vy0 = self.initial_state
        steps, dt = self.time_step
        if self.physics is None:
            return self._simulate_with_default_physics()
        coefficient_of_restitution, g = self.physics
        return self._simulate_with_custom_physics(coefficient_of_restitution, g)

    def _simulate_with_default_physics(self) -> list:
        x_positions = [self.initial_state[0]]
        y_positions = [self.initial_state[1]]
        vx = self.initial_state[2]
        vy = self.initial_state[3]
        for i in range(self.time_step[0]):
            x_positions.append(x_positions[-1] + vx * self.time_step[1])
            y_positions.append(y_positions[-1] + vy * self.time_step[1])
            if y_positions[-1] < 0:
                vy = -vy * 0.2
                y_positions[-1] = 0
            else:
                y_positions[-1] = y_positions[-1] + vy * self.time_step[1]
                vy = vy - 9.83 * self.time_step[1]
        return x_positions, y_positions

    def _simulate_with_custom_physics(self, coefficient_of_restitution, g) -> list:
        x_positions = [self.initial_state[0]]
        y_positions = [self.initial_state[1]]
        vx = self.initial_state[2]
        vy = self.initial_state[3]
        for i in range(self.time_step[0]):
            x_positions.append(x_positions[-1] + vx * self.time_step[1])
            y_positions.append(y_positions[-1] + vy * self.time_step[1])
            if y_positions[-1] < 0:
                vy = -vy * coefficient_of_restitution
                y_positions[-1] = 0
            else:
                y_positions[-1] = y_positions[-1] + vy * self.time_step[1]
                vy = vy - g * self.time_step[1]
        return x_positions, y_positions


def run(state, time, physics=None):
    """state: (x0, y0, vx0, vy0). time: (steps, dt). Public entry point of this unit.

    physics: (coefficient of restitution, gravity); without it, the default
    values of the simulation apply.
    """
    simulation = BouncingBallSimulation(state, time, physics)
    return simulation.simulate()
