import abc
import math
from dataclasses import dataclass
from typing import Protocol

import rev

from subsystems.elevator.elevator_constants import *


@dataclass
class ElevatorIOData:
    position_meters: float
    velocity_mps: float
    applied_voltage: float


class ElevatorIO(Protocol):
    inputs = ElevatorIOData(0, 0, 0)

    @abc.abstractmethod
    def update_inputs(self):
        raise NotImplementedError

    @abc.abstractmethod
    def run_position(self, position_meters: float):
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self):
        raise NotImplementedError


class ElevatorIOReal(ElevatorIO):
    def __init__(self):
        self.leader_motor = rev.SparkMax(LEFT_MOTOR_ID, rev.SparkMax.MotorType.kBrushless)
        self.follower_motor = rev.SparkMax(RIGHT_MOTOR_ID, rev.SparkMax.MotorType.kBrushless)
        self.controller = self.leader_motor.getClosedLoopController()
        self.encoder = self.leader_motor.getEncoder()

        global_config = rev.SparkBaseConfig()
        leader_config = rev.SparkBaseConfig()
        follower_config = rev.SparkBaseConfig()

        global_config \
            .setIdleMode(rev.SparkBaseConfig.IdleMode.kBrake) \
            .smartCurrentLimit(CURRENT_LIMIT)

        leader_config \
            .apply(global_config) \
            .inverted(INVERT_MOTORS)
        leader_config.encoder \
            .positionConversionFactor(2 * (1 / GEAR_RATIO) * (SPROCKET_PITCH_DIAMETER * math.pi)) \
            .velocityConversionFactor(2 * (1 / GEAR_RATIO) * (SPROCKET_PITCH_DIAMETER * math.pi) * (1 / 60))
        leader_config.closedLoop \
            .pid(kP, 0, 0)
        leader_config.softLimit \
            .forwardSoftLimit(MAXIMUM_CARRIAGE_HEIGHT - OFFSET_FROM_FLOOR) \
            .reverseSoftLimit(MINIMUM_CARRIAGE_HEIGHT - OFFSET_FROM_FLOOR) \
            .forwardSoftLimitEnabled(LIMITS_ENABLED) \
            .reverseSoftLimitEnabled(LIMITS_ENABLED)

        follower_config \
            .apply(global_config) \
            .follow(LEFT_MOTOR_ID, False)

        self.leader_motor.configure(
            leader_config, rev.SparkBase.ResetMode.kResetSafeParameters, rev.SparkBase.PersistMode.kPersistParameters
        )
        self.follower_motor.configure(
            follower_config, rev.SparkBase.ResetMode.kResetSafeParameters, rev.SparkBase.PersistMode.kPersistParameters
        )

        self.encoder.setPosition(0)

    def update_inputs(self):
        self.inputs = ElevatorIOData(
            position_meters=self.encoder.getPosition(),
            velocity_mps=self.encoder.getVelocity(),
            applied_voltage=self.leader_motor.getAppliedOutput() * self.leader_motor.getBusVoltage(),
        )

    def run_position(self, position_meters: float):
        self.controller.setReference(position_meters, rev.SparkBase.ControlType.kPosition)

    def stop(self):
        self.leader_motor.stopMotor()