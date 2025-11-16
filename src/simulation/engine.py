from simulation.models import DynamicModel
from simulation.signals import InputSignal
from simulation.logger import Logger
import numpy as np
import control as ct

class SimulationEngine:
    def __init__(self, model: DynamicModel, signal: InputSignal, logger: Logger):
        self.model = model
        self.signal = signal
        self.logger = logger

    def run_simulation(self, t_start: float, t_end: float, dt: float):
        time_vector = np.arange(t_start, t_end, dt)
        
        # Create a new model for the simulation
        # This is a bit of a hack, but it's the easiest way to use the control library
        # with the new architecture.
        model_tf = ct.tf([self.model.K], [self.model.tau, 1])
        
        input_signal_vector = [self.signal.get_value(t) for t in time_vector]

        t_out, y_out, _ = ct.forced_response(model_tf, T=time_vector, U=input_signal_vector, return_x=True)

        for t, y in zip(t_out, y_out):
            self.logger.log_data(t, y)
