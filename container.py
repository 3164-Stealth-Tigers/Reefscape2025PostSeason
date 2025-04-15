from commands2 import Command
from commands2.button import CommandXboxController
from wpilib import SendableChooser, SmartDashboard

from commands.elevator import ElevatorGoalHeightCommand
from lib.conversions import inches_to_meters
from subsystems.elevator.elevator import Elevator


class RobotContainer:
    def __init__(self):
        self.auto_chooser = SendableChooser()
        self.auto_chooser.setDefaultOption("Default", Command())
        SmartDashboard.putData("Auto Chooser", self.auto_chooser)

        self.joystick = CommandXboxController(0)

        # Make subsystems
        self.elevator = Elevator()

        # Bind buttons and other inputs to commands
        self.bind_triggers()

    def get_autonomous_command(self):
        return self.auto_chooser.getSelected()

    def bind_triggers(self):
        self.joystick.b().onTrue(ElevatorGoalHeightCommand(inches_to_meters(45)))
        self.joystick.a().onTrue(ElevatorGoalHeightCommand(inches_to_meters(55)))
        self.joystick.x().onTrue(ElevatorGoalHeightCommand(inches_to_meters(30.5)))
