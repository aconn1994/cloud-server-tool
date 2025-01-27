import os
import importlib

class GameConfigClient:
    def __init__(self, local_game_dir) -> None:
        self.local_game_dir: str = local_game_dir
        self.config: str = None
        self.workshop_items_list: str = None
        self._execute()

    def _get_configuration(self) -> dict[str, dict[str, str]]: # Convert to Python Model/Yaml File pattern?
        return {
            "arma_three": {
                "mod_file_path": os.path.join(self.local_game_dir, "mod-list.html"),
                "configuration_file_path": os.path.join(self.local_game_dir, "server.cfg"),
                "binary": "arma3server_x64",
            }
        } 

    def _execute(self) -> None:
        self.config = self._get_configuration()[self.local_game_dir]
        game_utils = importlib.import_module(f'{self.local_game_dir}.utils')

        if self.local_game_dir == 'arma_three':
            parsed_mod_list = game_utils.parse_mod_file(self.config['mod_file_path'])
