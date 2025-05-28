from abc import ABC, abstractmethod

from cst_game.os_manager.abstract_os import AbstractOS


class AbstractPlatformConfig(ABC):
    def __init__(self, os_manager: AbstractOS) -> None:
        self.os_manager = os_manager

    @property
    @abstractmethod
    def binary_32bit(self) -> str:
        pass

    @property
    @abstractmethod
    def binary_64bit(self) -> str:
        pass

    @property
    @abstractmethod
    def username(self) -> str | None:
        pass

    @property
    @abstractmethod
    def password(self) -> str | None:
        pass
