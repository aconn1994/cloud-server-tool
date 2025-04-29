from typing import Any


# Dummy GameUtil for intellisense until whl file is built
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
        self.local_game_assets_src = local_game_assets_src
        self.game_install_dst = game_install_dst
        self.game_id = "dummy_game_id"

    def execute(self):
        pass

    def launch(self):
        pass
