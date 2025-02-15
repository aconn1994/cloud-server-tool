import importlib as il
from typing import Any


class GameConfigClient:
    def __init__(
        self,
        local_game_dir: str,
        local_game_assets_dir: str,
        game_install_dir: str,
        steam_client: Any,
        utils: Any,
    ) -> None:
        self.local_game_dir = local_game_dir
        self.local_game_assets_dir: str = local_game_assets_dir
        self.game_install_dir: str = game_install_dir
        self.steam_client = steam_client
        self.utils = utils
        self.game_utils: il.ModuleType | None = None
        self.game_id: str | None = None

    def execute(self) -> None:
        # todo, dynamic import is bugged, may need to do whl packaging and install to docker file
        self.game_utils = il.import_module(
            f"{self.local_game_dir}.{self.local_game_dir}_util",
        )
        self.game_utils.ArmaThreeUtil(
            self.utils,
            self.steam_client,
            self.local_game_assets_dir,
            self.game_install_dir,
        )
        self.game_id = self.game_utils.game_id

    def handle_game_configuration(self) -> None:
        self.game_utils.execute()

    def launch(self) -> None:
        self.game_utils.launch()
