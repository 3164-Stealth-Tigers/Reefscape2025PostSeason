from commands2.button import CommandXboxController, Trigger

from oi.templates import OperatorTemplate


class XboxOperator(OperatorTemplate):
    def level_loading(self) -> Trigger:
        return self.joystick.rightTrigger()

    def level_1(self) -> Trigger:
        return self.joystick.a()

    def level_2(self) -> Trigger:
        return self.joystick.x()

    def level_3(self) -> Trigger:
        return self.joystick.b()

    def level_4(self) -> Trigger:
        return self.joystick.y()

    def __init__(self, port: int):
        self.joystick = CommandXboxController(port)