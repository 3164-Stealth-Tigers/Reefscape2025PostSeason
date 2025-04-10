from commands2 import Subsystem

from subsystems.elevator.elevator_io import ElevatorIOReal


class Elevator(Subsystem):
    def __init__(self):
        super().__init__()

        self.io = ElevatorIOReal()

    def set_height(self, height: float):
        """
        Commands the elevator to move to a certain height above the floor.
        :param height: Height above the floor in meters.
        """

    def get_height(self) -> float:
        """The current height of the elevator in meters above the floor."""

    def periodic(self) -> None:
        # Automatically called every 20ms

        # Update inputs from motors and sensors
        self.io.update_inputs()
