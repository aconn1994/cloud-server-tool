import os
from logging import Logger
from typing import Any

from cst_game.common.game_setup_runner_args import GameSetupRunnerArgs
from cst_game.games.arma_three.arma_three_html_parser import ArmaThreeHTMLParser
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

    @staticmethod
    def html_parser(reformat_string: Any) -> ArmaThreeHTMLParser:
        return ArmaThreeHTMLParser(reformat_string)

    @property
    def game_name(self) -> str:
        return "arma_three"

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

    # Directory/Pathing
    @property
    def game_install_path(self) -> str:
        return os.path.join(
            self.os_manager.instance_root_dir, "steamcmd", self.game_name
        )

    @property
    def game_assets_path(self) -> str:
        return os.path.join(self.os_manager.instance_root_dir, "assets")

    @property
    def key_dst_path(self) -> str:
        return os.path.join(self.game_install_path, "keys")

    @property
    def workshop_items_download_path(self) -> str:
        return os.path.join(self.game_install_path, self.workshop_items_path)

    # Cfg Paths
    @property
    def configuration_file_src_path(self) -> str:
        return os.path.join(self.game_assets_path, "server.cfg")

    @property
    def configuration_file_dst_path(self) -> str:
        return os.path.join(self.game_install_path, "server.cfg")

    # Profile Paths
    @property
    def profile_src_path(self) -> str:
        return os.path.join(self.game_assets_path, "server.Arma3Profile")

    @property
    def profile_dst_path(self) -> str:
        return os.path.join(self.game_install_path, "server", "server.Arma3Profile")

    # Mission Paths
    @property
    def missions_src_path(self) -> str:
        return os.path.join(self.game_assets_path, "missions")

    @property
    def missions_dst_path(self) -> str:
        return os.path.join(self.game_install_path, "mpmissions")

    # Mod Paths
    @property
    def mod_file_src_path(self) -> str:
        return os.path.join(self.game_assets_path, "mod-list.html")

    @property
    def mod_file_dst_path(self) -> str:
        return os.path.join(self.game_install_path, "mods")
