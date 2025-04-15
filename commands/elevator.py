import commands2

from subsystems.elevator.elevator import Elevator


def ElevatorGoalHeightCommand(height: float):
    elevator = Elevator()
    return commands2.InstantCommand(lambda: elevator.set_goal_height(height), elevator)
