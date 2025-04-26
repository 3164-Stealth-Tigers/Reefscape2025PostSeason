from commands2 import Command, SequentialCommandGroup, WaitUntilCommand, WaitCommand

from commands.elevator import ElevatorGoalHeightCommand
from lib.conversions import inches_to_meters
from subsystems.elevator.elevator import Elevator
from subsystems.elevator.elevator_constants import MINIMUM_CARRIAGE_HEIGHT


def get_example_auto() -> Command:
    elevator = Elevator()
    return SequentialCommandGroup(
        # Set elevator goal height to 40 inches
        ElevatorGoalHeightCommand(inches_to_meters(40)),
        # Wait for elevator to reach goal
        WaitUntilCommand(elevator.at_goal),
        # Wait 1 second
        WaitCommand(1),
        # Set the elevator goal height to 70 inches
        ElevatorGoalHeightCommand(inches_to_meters(70)),
        # Wait for elevator to reach goal
        WaitUntilCommand(elevator.at_goal),
        # Wait 1 sec
        WaitCommand(1),
        # Finally, Set the elevator goal height to minimum height
        ElevatorGoalHeightCommand(MINIMUM_CARRIAGE_HEIGHT)
    )
