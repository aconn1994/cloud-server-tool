import getpass
import os
import platform
from abc import ABC, abstractmethod


class AbstractOS(ABC):
    @property
    @abstractmethod
    def operating_system_alias(self) -> str:
        pass

    @property
    def operating_system_name(self) -> str:
        return os.name

    @property
    def platform_system(self) -> str:
        return platform.system()

    @property
    def system_version(self) -> str:
        return platform.release()

    @property
    def user(self) -> str:
        return getpass.getuser()

    @property
    @abstractmethod
    def instance_root_dir(self) -> str:
        pass
