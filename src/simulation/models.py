from abc import ABC, abstractmethod
import control as ct

class DynamicModel(ABC):
    @abstractmethod
    def get_params(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_response(self, input_value: float) -> float:
        raise NotImplementedError

class WaterTankModel(DynamicModel):
    def __init__(self, K: float, tau: float):
        self.K = K
        self.tau = tau
        self.model = ct.tf([self.K], [self.tau, 1])

    def get_params(self) -> dict:
        return {"K": self.K, "tau": self.tau}

    def get_response(self, input_value: float) -> float:
        # For a first-order system, the response to a step input can be calculated analytically.
        # However, to keep it general, we can simulate a small time step.
        # This is not the most efficient way, but it demonstrates the principle.
        t = [0, 0.1] # small time step
        _, y = ct.forced_response(self.model, T=t, U=input_value)
        return y[1]
