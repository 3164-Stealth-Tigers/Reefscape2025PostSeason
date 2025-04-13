from commands2 import Subsystem

from subsystems.elevator.elevator_constants import *
from subsystems.elevator.elevator_io import ElevatorIOReal
from lib.singleton import MetaSingletonSubsystem
from wpimath.trajectory import TrapezoidProfile


class Elevator(Subsystem, metaclass=MetaSingletonSubsystem):
    def __init__(self):
        super().__init__()

        self.io = ElevatorIOReal()

        self.profile = TrapezoidProfile(TrapezoidProfile.Constraints(MAX_VELOCITY, MAX_ACCELERATION))
        self.goal = TrapezoidProfile.State()
        self.setpoint = TrapezoidProfile.State()

    def set_goal_height(self, height: float):
        """
        Commands the elevator to move to a certain height above the floor.
        :param height: Height above the floor in meters.
        """
        self.goal = TrapezoidProfile.State(height)

    def get_height(self) -> float:
        """The current height of the elevator in meters above the floor."""
        return self.io.inputs.position_meters

    def get_velocity(self) -> float:
        """The current velocity of the elevator in meters/sec."""

    def periodic(self) -> None:
        # Automatically called every 20ms

        # Update inputs from motors and sensors
        self.io.update_inputs()

        # Update setpoint with profile
        should_run_profile = MINIMUM_CARRIAGE_HEIGHT <= self.goal.position <= MAXIMUM_CARRIAGE_HEIGHT
        if should_run_profile:
            self.setpoint = self.profile.calculate(0.02, self.setpoint, self.goal)

        # Run motors
        self.io.run_position(self.setpoint.position)
