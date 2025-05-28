import os
from abc import abstractmethod

from cst_game.common.clients.steam_cmd_client import SteamCMDClient
from cst_game.os_manager.abstract_os import AbstractOS
from cst_game.platform_config.abstract_platform_config import AbstractPlatformConfig


class SteamConfig(AbstractPlatformConfig):
    def __init__(self, os_manager: AbstractOS) -> None:
        self.os_manager = os_manager
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
    def workshop_items_download_path(self) -> str:
        return os.path.join("steamapps", "workshop", "content", self.game_workshop_id)

    def steam_client(self, os_manager: AbstractOS) -> SteamCMDClient:
        return SteamCMDClient(
            os_manager.instance_root_dir, self.username, self.password
        )

    @staticmethod
    def steamcmd_root_dir(instance_root_dir: str) -> str:
        return os.path.join(instance_root_dir, "steamcmd")

    def install_steamcmd_binary(self, instance_root_dir: str) -> None:
        pass  # todo, get and unpack steamcmd based on operating system
