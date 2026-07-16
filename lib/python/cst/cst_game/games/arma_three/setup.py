import os
import shutil
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
        if os.path.exists(self.game_config.configuration_file_src_path):
            shutil.copyfile(
                self.game_config.configuration_file_src_path,
                self.game_config.configuration_file_dst_path,
            )
            self.logger.info(
                f"Server config placed at {self.game_config.configuration_file_dst_path}"
            )

        if os.path.exists(self.game_config.profile_src_path):
            os.makedirs(self.game_config.profiles_dst_path, exist_ok=True)
            shutil.copyfile(
                self.game_config.profile_src_path,
                self.game_config.profile_dst_path,
            )
            self.logger.info(f"Server profile placed at {self.game_config.profile_dst_path}")
            if os.path.exists(self.game_config.profile_vars_src_path):
                shutil.copyfile(
                    self.game_config.profile_vars_src_path,
                    self.game_config.profile_vars_dst_path,
                )

        if os.path.exists(self.game_config.missions_src_path):
            self.symlink(
                self.game_config.missions_src_path,
                self.game_config.missions_dst_path,
                descriptor="Missions",
            )

    def _setup_steam_client_libraries(self) -> None:
        steamcmd_dir = self.game_config.steamcmd_root_dir(
            self.game_config.os_manager.instance_root_dir
        )
        home_dir = os.path.expanduser("~")
        for arch, steam_lib_dir in (("32", "linux32"), ("64", "linux64")):
            sdk_dir = os.path.join(home_dir, ".steam", f"sdk{arch}")
            os.makedirs(sdk_dir, exist_ok=True)
            self.symlink(
                os.path.join(steamcmd_dir, steam_lib_dir, "steamclient.so"),
                os.path.join(sdk_dir, "steamclient.so"),
                descriptor=f"Steam client library ({steam_lib_dir})",
            )

    def _write_steam_appid(self) -> None:
        with open(self.game_config.steam_appid_file_path, "w") as appid_file:
            appid_file.write(self.game_config.steam_appid)

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
        launch_cmd.extend([f"-name={self.game_config.profile_name}"])
        launch_cmd.extend([f"-profiles={self.game_config.profiles_root_path}"])
        launch_cmd.extend([f"-config={self.game_config.configuration_file_dst_path}"])
        launch_cmd.extend([f"-port={self.game_config.game_port}"])

        if self.game_config.dlcs:
            for dlc_name in self.game_config.dlcs.split(","):
                launch_cmd.extend([f"-mod={dlc_name}"])

        if self.launch_with_mods:
            for workshop_item_name in self.workshop_items.keys():
                launch_cmd.extend([f"-mod=mods/@{workshop_item_name.lower()}"])

        print(" ".join(launch_cmd))
        subprocess.call(launch_cmd)

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        self.logger.info(f"Executing {self.name()}...")

        if not self.parsed_args.expedite_launch:  # todo, TEST THIS NEXT
            # Install SteamCMD
            self.game_config.install_steamcmd_binary()

            # Install Game (Arma 3)
            if not os.path.exists(self.game_config.game_install_path):
                os.makedirs(self.game_config.game_install_path, exist_ok=True)

            if self.game_config.dlcs:
                beta_arg = "creatordlc"
            else:
                beta_arg = None

            self.steam_cmd_client.install_game(self.game_config.game_id, beta_arg)

            # Server Configuration (Required files, modding etc)
            self._link_game_config_files()
            if os.path.exists(self.game_config.mod_file_src_path) and (
                self.steam_cmd_client.has_credentials
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
        else:
            self._link_game_config_files()
            if os.path.exists(self.game_config.mod_file_dst_path):
                self._parse_mod_file()
                self.launch_with_mods = True

        self._setup_steam_client_libraries()
        self._write_steam_appid()

        # Launch Game
        if os.path.exists(
            os.path.join(self.game_config.game_install_path, self.game_config.binary_32bit)
        ) or os.path.exists(
            os.path.join(self.game_config.game_install_path, self.game_config.binary_64bit)
        ):
            self._launch_game()
            self.logger.info(f"{self.name()} has been Executed.")
        else:
            self.logger.info(
                f"Game binaries for {self.name()} not found. Check Steam Authentication."
            )


def main(parsed_args: GameSetupRunnerArgs) -> None:
    Setup(parsed_args=parsed_args).execute()
