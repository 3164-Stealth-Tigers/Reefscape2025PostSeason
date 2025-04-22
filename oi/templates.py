"""Action Sets / Templates"""
from abc import abstractmethod
from typing import Protocol

from commands2.button import Trigger


class OperatorTemplate(Protocol):
    @abstractmethod
    def level_loading(self) -> Trigger:
        """Move the elevator to loading level."""

    @abstractmethod
    def level_1(self) -> Trigger:
        """Move the elevator to level 1."""

    @abstractmethod
    def level_2(self) -> Trigger:
        """Move the elevator to level 2."""

    @abstractmethod
    def level_3(self) -> Trigger:
        """Move the elevator to level 3."""

    @abstractmethod
    def level_4(self) -> Trigger:
        """Move the elevator to level 4."""