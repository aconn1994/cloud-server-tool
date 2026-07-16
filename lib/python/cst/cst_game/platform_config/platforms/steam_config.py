import os
import subprocess
from abc import abstractmethod
from logging import Logger

from cst_game.common.clients.steam_cmd_client import SteamCMDClient
from cst_game.common.game_setup_runner_args import GameSetupRunnerArgs
from cst_game.os_manager.abstract_os import AbstractOS
from cst_game.platform_config.abstract_platform_config import AbstractPlatformConfig


class SteamConfig(AbstractPlatformConfig):
    def __init__(
        self, parsed_args: GameSetupRunnerArgs, os_manager: AbstractOS, logger: Logger
    ) -> None:
        self.parsed_args = parsed_args
        self.os_manager = os_manager
        self.logger = logger
        super().__init__(self.os_manager)

    @property
    def platform_name(self) -> str:
        return "steam"

    @property
    @abstractmethod
    def game_id(self) -> str:
        pass

    @property
    @abstractmethod
    def game_workshop_id(self) -> str:
        pass

    @property
    def workshop_items_path(self) -> str:
        return os.path.join("steamapps", "workshop", "content", self.game_workshop_id)

    def steam_client(self, game_install_dir: str) -> SteamCMDClient:
        return SteamCMDClient(
            game_install_dir,
            self.parsed_args.username,
            self.parsed_args.password,
        )

    @staticmethod
    def steamcmd_root_dir(instance_root_dir: str) -> str:
        return os.path.join(instance_root_dir, "steamcmd")

    def install_steamcmd_binary(self) -> None:  # pragma: no cover
        if self.parsed_args.operating_system == "linux":
            steamcmd_dir = self.steamcmd_root_dir(self.os_manager.instance_root_dir)
            os.makedirs(steamcmd_dir, exist_ok=True)
            subprocess.run(
                "curl -sqL 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz'"
                f" | tar zxf - -C {steamcmd_dir}",
                shell=True,
                check=True,
            )
        elif self.parsed_args.operating_system == "windows":
            pass
        else:
            self.logger.warning("Operating System not supported.")
