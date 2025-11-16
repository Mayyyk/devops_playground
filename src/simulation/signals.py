from abc import ABC, abstractmethod

class InputSignal(ABC):
    @abstractmethod
    def get_value(self, time: float) -> float:
        raise NotImplementedError

class StepSignal(InputSignal):
    def __init__(self, amplitude: float):
        self.amplitude = amplitude

    def get_value(self, time: float) -> float:
        return self.amplitude
