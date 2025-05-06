from abc import ABC, abstractmethod


class AbstractPlatformConfig(ABC):
    def __init__(self) -> None:
        super().__init__()

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
