import os
import subprocess
from abc import ABC
from typing import Any

from cst_game.common.abstract_game_setup import AbstractGameSetup
from cst_game.common.game_setup_runner_args import GameSetupRunnerArgs
from cst_game.games.arma_three.game_config import GameConfig


class Setup(AbstractGameSetup, ABC):
    def __init__(self, parsed_args: GameSetupRunnerArgs) -> None:
        super().__init__(parsed_args=parsed_args)
        self.logger = self.init_logger()
        self.game_config = GameConfig(self.parsed_args, self.logger)
        self.os_manager = self.game_config.os_manager
        self.steam_cmd_client = self.game_config.steam_client(self.game_config.game_install_path)
        self.html_parser = self.game_config.html_parser(self.reformat_string)
        self.workshop_items: dict[str, str] | None = None
        self.launch_with_mods: bool = False

    def name(self) -> str:
        return "Arma 3 Game Server Setup"

    def _link_game_config_files(self) -> None:
        # Symlink Server Config File
        if os.path.exists(self.game_config.configuration_file_src_path):
            self.symlink(
                self.game_config.configuration_file_src_path,
                self.game_config.configuration_file_dst_path,
                descriptor="Server Config",
            )

        # Symlink Server Profile
        if os.path.exists(self.game_config.profile_src_path):
            if not os.path.exists(os.path.join(self.game_config.game_install_path, "server")):
                os.mkdir(os.path.join(self.game_config.game_install_path, "server"))
            self.symlink(
                self.game_config.profile_src_path,
                self.game_config.profile_dst_path,
                descriptor="Server Profile",
            )

        # Symlink Missions
        if os.path.exists(self.game_config.missions_src_path):
            self.symlink(
                self.game_config.missions_src_path,
                self.game_config.missions_dst_path,  # todo, showing "missions already linked" and dir is empty
                descriptor="Missions",
            )

    def _parse_mod_file(self) -> None:
        mod_file = open(self.game_config.mod_file_src_path, "r")
        self.html_parser.feed(mod_file.read())
        self.workshop_items = self.html_parser.html_as_dict

    def _download_workshop_item(self, workshop_item_id: str) -> None:
        self.steam_cmd_client.download_workshop_mod(
            self.game_config.game_workshop_id, workshop_item_id
        )

    def _link_workshop_item(
        self, workshop_item_name: str, workshop_item_download_path: str
    ) -> None:
        self.recursive_rename_directory(workshop_item_download_path, case="lower")
        self.symlink(
            workshop_item_download_path,
            os.path.join(self.game_config.mod_file_dst_path, f"@{workshop_item_name.lower()}"),
            descriptor="Mod",
        )

    def _link_key_item(self, workshop_item_download_path: str) -> None:
        steam_workshop_path_with_key = [
            entity for entity in os.listdir(workshop_item_download_path) if "key" in entity
        ]
        steam_workshop_keys_path = os.path.join(
            workshop_item_download_path, steam_workshop_path_with_key[-1]
        )
        workshop_item_key_name = os.listdir(steam_workshop_keys_path)[0]
        self.symlink(
            os.path.join(steam_workshop_keys_path, workshop_item_key_name),
            os.path.join(self.game_config.key_dst_path, workshop_item_key_name),
            descriptor="Key",
        )

    def _launch_game(self) -> None:
        os.chdir(self.game_config.game_install_path)
        if self.parsed_args.arch == "32":
            launch_cmd = ["./" + self.game_config.binary_32bit]
        else:
            launch_cmd = ["./" + self.game_config.binary_64bit]
        launch_cmd.extend(["-name=server"])
        if self.launch_with_mods:
            for workshop_item_name in self.workshop_items.keys():
                launch_cmd.extend([f"-mod=mods/@{workshop_item_name.lower()}"])

        launch_cmd.extend(["-config=server.cfg"])

        print(" ".join(launch_cmd))
        subprocess.call(launch_cmd)

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        self.logger.info(f"Executing {self.name()}...")

        # Install SteamCMD
        self.game_config.install_steamcmd_binary()

        # Install Game (Arma 3)
        if not os.path.exists(self.game_config.game_install_path):
            os.mkdir(self.game_config.game_install_path)
        self.steam_cmd_client.install_game(self.game_config.game_id)

        # Server Configuration (Required files, modding etc)
        self._link_game_config_files()
        if os.path.exists(self.game_config.mod_file_src_path) and (
            self.parsed_args.username is not None and self.parsed_args.password is not None
        ):
            self.launch_with_mods = True
            if not os.path.exists(self.game_config.mod_file_dst_path):
                os.mkdir(self.game_config.mod_file_dst_path)
            self._parse_mod_file()
            for workshop_item_name, workshop_item_id in self.workshop_items.items():
                self._download_workshop_item(workshop_item_id)
                workshop_item_download_path = os.path.join(
                    self.game_config.workshop_items_download_path, workshop_item_id
                )
                self._link_workshop_item(workshop_item_name, workshop_item_download_path)
                self._link_key_item(workshop_item_download_path)

        # Launch Game
        self._launch_game()

        self.logger.info(f"{self.name()} has been Executed.")


def main(parsed_args: GameSetupRunnerArgs) -> None:
    Setup(parsed_args=parsed_args).execute()
