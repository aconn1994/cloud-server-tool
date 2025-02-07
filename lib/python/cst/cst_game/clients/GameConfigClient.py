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

    def handle_mod_configuration(self,) -> None:
            # todo, need to test pathing for mod download, add symlinks
            pass