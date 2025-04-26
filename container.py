from commands2 import Command
from wpilib import SendableChooser, SmartDashboard

from commands.autos.example_auto import get_example_auto
from commands.elevator import ElevatorGoalHeightCommand
from lib.conversions import inches_to_meters
from oi.schemes import XboxOperator
from subsystems.elevator.elevator import Elevator


class RobotContainer:
    def __init__(self):
        self.auto_chooser = SendableChooser()
        self.auto_chooser.setDefaultOption("Default", get_example_auto())
        SmartDashboard.putData("Auto Chooser", self.auto_chooser)

        self.joystick = XboxOperator(1)

        # Make subsystems
        self.elevator = Elevator()

        # Bind buttons and other inputs to commands
        self.bind_triggers()

    def get_autonomous_command(self):
        return self.auto_chooser.getSelected()

    def bind_triggers(self):
        self.joystick.level_loading().onTrue(ElevatorGoalHeightCommand(inches_to_meters(30.5)))
        self.joystick.level_1().onTrue(ElevatorGoalHeightCommand(inches_to_meters(42.5)))
        self.joystick.level_2().onTrue(ElevatorGoalHeightCommand(inches_to_meters(55)))
        self.joystick.level_3().onTrue(ElevatorGoalHeightCommand(inches_to_meters(67.5)))
        self.joystick.level_4().onTrue(ElevatorGoalHeightCommand(inches_to_meters(80)))
