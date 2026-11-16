class BouncingBallSimulation:
    def __init__(self, initial_state, time_parameters, physical_constants=None):
        self.initial_state = initial_state
        self.time_parameters = time_parameters
        self.physical_constants = physical_constants

    def simulate(self):
        x0, y0, vx0, vy0 = self.initial_state
        steps, dt = self.time_parameters
        if self.physical_constants is None:
            return self._simulate(x0, y0, vx0, vy0, steps, dt)
        coefficient_of_restitution, g = self.physical_constants
        return self._simulate(x0, y0, vx0, vy0, steps, dt, coefficient_of_restitution, g)

    def _simulate(self, x0, y0, vx0, vy0, steps, dt, coefficient_of_restitution=0.2, g=9.83):
        x_positions = [x0]
        y_positions = [y0]
        vx = vx0
        vy = vy0
        for i in range(steps):
            x_positions.append(x_positions[-1] + vx * dt)
            y_positions.append(y_positions[-1] + vy * dt)
            if y_positions[-1] < 0:
                vy = -vy * coefficient_of_restitution
                y_positions[-1] = 0
            else:
                y_positions[-1] = y_positions[-1] + vy * dt
                vy = vy - g * dt
        return x_positions, y_positions

def executar(estado, tempo, fisica=None):
    simulation = BouncingBallSimulation(estado, tempo, fisica)
    return simulation.simulate()
