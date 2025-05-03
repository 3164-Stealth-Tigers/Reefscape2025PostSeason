import abc
import math
from dataclasses import dataclass
from typing import Protocol

from wpilib import RobotController
from wpilib.simulation import ElevatorSim
from wpimath.controller import PIDController
from wpimath.system.plant import DCMotor, LinearSystemId
import rev

from lib.math_extensions import clamp
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


class ElevatorIOSim(ElevatorIO):
    def __init__(self):
        self.gearbox = DCMotor.NEO(2).withReduction(GEAR_RATIO)
        self.plant = LinearSystemId.elevatorSystem(self.gearbox, CARRIAGE_MASS, SPROCKET_PITCH_DIAMETER / 2, 1)
        self.elevator_sim = ElevatorSim(
            self.plant,
            self.gearbox,
            0,
            MAXIMUM_CARRIAGE_HEIGHT - MINIMUM_CARRIAGE_HEIGHT,
            True,
            0,
        )
        self.controller = PIDController(kP, 0, 0)

        self.voltage_out = 0
        self.closed_loop = False

    def update_inputs(self):
        # Update the simulation and PID controller
        self.update(0.02)

        self.inputs = ElevatorIOData(
            position_meters=self.elevator_sim.getPosition(),
            velocity_mps=self.elevator_sim.getVelocity(),
            applied_voltage=self.voltage_out,
        )

    def run_position(self, position_meters: float):
        self.closed_loop = True
        self.controller.setSetpoint(position_meters)

    def stop(self):
        self.closed_loop = False
        self.voltage_out = 0

    def update(self, dt: float):
        # Calculate output voltage from PID controller
        if self.closed_loop:
            percent_out = clamp(self.controller.calculate(self.elevator_sim.getPosition()), -1, 1)
            self.voltage_out = percent_out * RobotController.getBatteryVoltage()

        self.elevator_sim.setInputVoltage(self.voltage_out)
        self.elevator_sim.update(dt)

