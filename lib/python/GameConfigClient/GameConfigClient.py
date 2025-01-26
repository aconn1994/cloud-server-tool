import os

class GameConfigClient:
    def __init__(self, local_game_dir) -> None:
        self.local_game_dir = local_game_dir
        self.config = None
        self.workshop_items_list = None
        self._execute()

    def _parse_mod_list(self, local_game_dir):
        pass

    def _get_configuration(self): # Convert to Python Model/Yaml File pattern?
        return {
            "arma3": {
                "mod_file_path": os.path.join(self.local_game_dir, "mod_list.html"),
                "configuration_file_path": os.path.join(self.local_game_dir, "server.cfg"),
                "binary": "arma3server_x64",
                "mod_list": self._parse_mod_list(self.local_game_dir)
            }
        } 

    def _execute(self) -> None:
        self.config = self._get_configuration()[self.local_game_dir]
