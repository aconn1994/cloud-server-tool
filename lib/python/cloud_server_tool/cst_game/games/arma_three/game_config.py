from logging import Logger

from cst_game.common.game_setup_runner_args import GameSetupRunnerArgs
from cst_game.os_manager.abstract_os import AbstractOS
from cst_game.os_manager.operating_system_manager import OperatingSystemManager
from cst_game.platform_config.platforms.steam_config import SteamConfig


class GameConfig(SteamConfig):
    def __init__(self, parsed_args: GameSetupRunnerArgs, logger: Logger) -> None:
        self.parsed_args = parsed_args
        self.logger = logger
        self.os_manager = self.get_os_manager(self.parsed_args.operating_system)
        super().__init__(self.parsed_args, self.os_manager, self.logger)

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
