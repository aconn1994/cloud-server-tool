from cst_game.os_manager.abstract_os import AbstractOS
from cst_game.os_manager.operating_system_manager import OperatingSystemManager
from cst_game.platform_config.platforms.steam_config import SteamConfig


class GameConfig(SteamConfig):
    def __init__(self, operating_system: str) -> None:
        self.os_manager = self.get_os_manager(operating_system)
        super().__init__(self.os_manager)

    @staticmethod
    def get_os_manager(operating_system: str) -> AbstractOS:
        os_manager = OperatingSystemManager()
        return os_manager.name_to_os_mapper[operating_system]

    @property
    def game_id(self) -> str:
        return "233780"

    @property
    def game_workshop_id(self) -> str:
        return "107410"

    @property
    def binary_32bit(self) -> str:
        return "arma3server_x32"

    @property
    def binary_64bit(self) -> str:
        return "arma3server_x64"

    @property
    def username(self) -> str | None:
        return None

    @property
    def password(self) -> str | None:
        return None
