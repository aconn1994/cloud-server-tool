import os
from typing import Any
from .arma_three_html_parser import ArmaThreeHTMLParser
import subprocess


class GameUtil:
    def __init__(
        self,
        utils: Any,
        steam_client: Any,
        local_game_assets_src: str,
        game_install_dst: str,
    ):
        self.utils = utils
        self.steam_client = steam_client
        self.arma_three_html_parser = ArmaThreeHTMLParser(self.utils)
        self.workshop_items: dict[str, str] | None = None

        # Game Variables
        self.game_id = "233780"
        self.workshop_id = "107410"
        self.workshop_items_download_path = os.path.join(
            game_install_dst, "steamapps", "workshop", "content"
        )
        self.binary = "arma3server_x64"
        self.game_install_dst_path = game_install_dst
        self.game_assets_src_path = os.path.join(local_game_assets_src, "assets")
        self.keys_dst = os.path.join(game_install_dst, "keys")

        # Cfg Paths
        self.configuration_src_file_path = os.path.join(
            self.game_assets_src_path, "server.cfg"
        )
        self.configuration_dst_file_path = os.path.join(
            self.game_install_dst_path, "server.cfg"
        )

        # Profile Paths
        self.profile_src_file_path = os.path.join(
            self.game_assets_src_path, "server.Arma3Profile"
        )
        self.profile_src_file_path = os.path.join(
            self.game_install_dst_path, "server", "server.Arma3Profile"
        )

        # Missions Paths
        self.game_missions_src_path = os.path.join(
            self.game_assets_src_path, "missions"
        )
        self.game_missions_dst_path = os.path.join(game_install_dst, "mpmissions")

        # Workshop Item/Mod Paths
        self.mod_src_file_path = os.path.join(
            self.game_assets_src_path, "mod-list.html"
        )
        self.mods_dst = os.path.join(game_install_dst, "mods")

    def _parse_mod_file(self, mod_file_path: str) -> None:
        mf = open(mod_file_path, "r")
        self.arma_three_html_parser.feed(mf.read())
        self.workshop_items = self.arma_three_html_parser.html_as_dict

    def _key_handler(self, workshop_item_download_path: str) -> None:
        steam_workshop_path_with_key = [
            entity
            for entity in os.listdir(workshop_item_download_path)
            if "key" in entity
        ]
        steam_workshop_keys_path = os.path.join(
            workshop_item_download_path, steam_workshop_path_with_key[-1]
        )
        workshop_item_key_name = os.listdir(steam_workshop_keys_path)[0]
        self.utils.symlink(
            os.path.join(steam_workshop_keys_path, workshop_item_key_name),
            os.path.join(self.keys_dst, workshop_item_key_name),
            descriptor="Key",
        )

    def _handle_workshop_items(
        self, workshop_item_name: str, workshop_item_id: str
    ) -> None:
        if not os.path.exists(self.mods_dst):
            os.makedirs(self.mods_dst)
        self.steam_client.download_workshop_mod(self.workshop_id, workshop_item_id)
        workshop_item_download_path = os.path.join(
            self.workshop_items_download_path, self.workshop_id, workshop_item_id
        )
        self.utils.recursive_rename_directory(workshop_item_download_path, case="lower")
        self.utils.symlink(
            workshop_item_download_path,
            os.path.join(self.mods_dst, f"@{workshop_item_name.lower()}"),
            descriptor="Mod",
        )
        self._key_handler(workshop_item_download_path)

    def execute(self):
        # Symlink Server Config File
        if os.path.exists(self.configuration_src_file_path):
            self.utils.symlink(
                self.configuration_src_file_path,
                self.configuration_dst_file_path,
                descriptor="Server Config",
            )

        # Symlink Server Profile
        if os.path.exists(self.profile_src_file_path):
            self.utils.symlink(
                self.profile_src_file_path,
                self.profile_src_file_path,
                descriptor="Server Profile",
            )

        # Symlink Missions:
        if os.path.exists(self.game_missions_src_path):
            self.utils.symlink(
                self.game_missions_src_path,
                self.game_missions_dst_path,
                descriptor="Mission",
            )

        # Workshop Item Handler
        if os.path.exists(self.mod_src_file_path):
            self._parse_mod_file(self.mod_src_file_path)
            for workshop_item_name, workshop_item_id in self.workshop_items.items():
                self._handle_workshop_items(workshop_item_name, workshop_item_id)

    def launch(self):
        os.chdir(self.game_install_dst_path)
        launch_cmd = ["./" + self.binary]
        launch_cmd.extend(["-name=server"])
        for workshop_item_name in self.workshop_items.keys():
            launch_cmd.extend([f"-mod=mods/@{workshop_item_name.lower()}"])

        launch_cmd.extend(["-config=server.cfg"])

        print(" ".join(launch_cmd))
        subprocess.call(launch_cmd)
