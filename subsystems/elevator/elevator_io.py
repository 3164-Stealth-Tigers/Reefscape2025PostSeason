import abc
from dataclasses import dataclass
from typing import Protocol


@dataclass
class ElevatorIOData:
    position_meters: float
    velocity_mps: float


class ElevatorIO(Protocol):
    inputs = ElevatorIOData(0, 0)

    @abc.abstractmethod
    def update_inputs(self):
        raise NotImplementedError

    @abc.abstractmethod
    def run_position(self, position_meters: float):
        raise NotImplementedError


class ElevatorIOReal(ElevatorIO):
    def update_inputs(self):
        pass

    def run_position(self, position_meters: float):
        pass