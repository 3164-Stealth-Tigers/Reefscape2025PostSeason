from commands2 import Command
from wpilib import SendableChooser, SmartDashboard

from subsystems.elevator.elevator import Elevator


class RobotContainer:
    def __init__(self):
        self.auto_chooser = SendableChooser()
        self.auto_chooser.setDefaultOption("Default", Command())
        SmartDashboard.putData("Auto Chooser", self.auto_chooser)

        # Make subsystems
        self.elevator = Elevator()

    def get_autonomous_command(self):
        return self.auto_chooser.getSelected()