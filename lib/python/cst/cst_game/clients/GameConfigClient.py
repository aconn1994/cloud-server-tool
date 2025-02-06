import os
import importlib
from typing import Any


class GameConfigClient:
    def __init__(self, local_game_dir: str) -> None:
        self.local_game_dir: str = local_game_dir
        self.config: str | None = None
        self.workshop_items_dict: dict[str, str] | None = None
        self._execute()

    def _get_configuration(
        self,
    ) -> dict[str, dict[str, str]]:  # Convert to Python Model/Yaml File pattern?
        return {
            "arma_three": {
                "mod_file_path": os.path.join(self.local_game_dir, "mod-list.html"),
                "configuration_file_path": os.path.join(
                    self.local_game_dir, "server.cfg"
                ),
                "binary": "arma3server_x64",
            }
        }

    def _execute(self) -> None:
        self.config = self._get_configuration()[self.local_game_dir]
        game_utils = importlib.import_module(f"{self.local_game_dir}.utils")

        if self.local_game_dir == "arma_three" and os.path.exists(
            self.config["mod_file_path"]
        ):
            self.workshop_items_dict = game_utils.parse_mod_file(
                self.config["mod_file_path"]
            )

    def handle_mod_configuration(
        self,
        steam_client: Any,
        game_server_id: str,
        local_game_dir: str,
        local_mod_dir: str,
        steam_workshop_dir: str,
    ) -> None:
        for display_name, workshop_item_id in self.workshop_items_dict.items():
            steam_client.download_workshop_mod(game_server_id, workshop_item_id)
            # todo, need to test pathing for mod download, add symlinks
