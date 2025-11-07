import control as ct
import numpy as np

class DynamicModel:
    """Abstrakcyjna klasa bazowa dla modeli."""
    def __init__(self):
        self.model = None

    def get_params(self):
        raise NotImplementedError

    def run_step_response(self, time_vector):
        raise NotImplementedError

class WaterTankModel(DynamicModel):
    """Implementacja modelu zbiornika pierwszego rzędu."""
    def __init__(self, K, tau):
        super().__init__()
        self.K = K
        self.tau = tau
        self.model = ct.tf([self.K], [self.tau, 1])

    def get_params(self):
        return {
            "K": self.K, 
            "tau": self.tau,
            "tf_string": str(self.model).strip()
        }

    def run_step_response(self, time_vector):
        t_out, y_out = ct.step_response(self.model, T=time_vector)
        return {
            "time_s": list(t_out),
            "temperature": list(y_out)
        }