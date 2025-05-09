from commands2 import Subsystem
from wpilib import SmartDashboard, RobotBase, DriverStation

from subsystems.elevator.elevator_constants import *
from subsystems.elevator.elevator_io import ElevatorIOReal, ElevatorIOSim
from lib.singleton import MetaSingletonSubsystem
from wpimath.trajectory import TrapezoidProfile


class Elevator(Subsystem, metaclass=MetaSingletonSubsystem):
    def __init__(self):
        super().__init__()

        self.io = ElevatorIOReal() if RobotBase.isReal() else ElevatorIOSim()

        self.profile = TrapezoidProfile(TrapezoidProfile.Constraints(MAX_VELOCITY, MAX_ACCELERATION))
        self.goal = TrapezoidProfile.State()
        self.setpoint = TrapezoidProfile.State()
        self.safety_stopped = False

    def set_goal_height(self, height: float):
        """
        Commands the elevator to move to a certain height above the floor.
        :param height: Height above the floor in meters.
        """
        self.goal = TrapezoidProfile.State(height - OFFSET_FROM_FLOOR)
        self.safety_stopped = False

    def get_height(self) -> float:
        """The current height of the elevator in meters above the floor."""
        return self.io.inputs.position_meters + OFFSET_FROM_FLOOR

    def get_velocity(self) -> float:
        """The current velocity of the elevator in meters/sec."""
        return self.io.inputs.velocity_mps

    def at_goal(self) -> bool:
        return abs(self.io.inputs.position_meters - self.goal.position) <= inches_to_meters(1)

    def periodic(self) -> None:
        # Automatically called every 20ms

        # Update inputs from motors and sensors
        self.io.update_inputs()

        # Logging
        SmartDashboard.putNumber("Elevator/GoalPosition", self.goal.position)
        SmartDashboard.putNumber("Elevator/SetpointPosition", self.setpoint.position)
        SmartDashboard.putNumber("Elevator/PositionNoOffset", self.io.inputs.position_meters)
        SmartDashboard.putNumber("Elevator/PositionWithOffset", self.get_height())
        SmartDashboard.putNumber("Elevator/Velocity", self.get_velocity())
        SmartDashboard.putNumber("Elevator/AppliedVoltage", self.io.inputs.applied_voltage)
        SmartDashboard.putBoolean("Elevator/AtGoal", self.at_goal())

        # Prevent the elevator from raising by itself after being Disabled --> Enabled
        if DriverStation.isDisabled():
            self.safety_stopped = True

        # Update setpoint with profile
        should_run_profile = (
                MINIMUM_CARRIAGE_HEIGHT - OFFSET_FROM_FLOOR <= self.goal.position <= MAXIMUM_CARRIAGE_HEIGHT - OFFSET_FROM_FLOOR
        )
        if should_run_profile:
            self.setpoint = self.profile.calculate(0.02, self.setpoint, self.goal)

        # Run motors
        if self.safety_stopped:
            self.io.stop()
        else:
            self.io.run_position(self.setpoint.position)
