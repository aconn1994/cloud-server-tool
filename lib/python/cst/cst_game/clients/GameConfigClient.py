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
        self.config: dict[str, str] | None = None
        self.workshop_items_dict: dict[str, str] | None = None

    # def _get_configuration(self) -> dict[str, str]:
    #     return self.game_utils.get_configuration(
    #         self.local_game_assets_dir, self.game_install_dir
    #     )

    def execute(self) -> None:
        self.game_utils = il.import_module(
            f"{self.local_game_dir}.{self.local_game_dir}_utils"
        )
        self.game_utils.initialize(
            self.utils,
            self.steam_client,
            self.local_game_assets_dir,
            self.game_install_dir,
        )

    def handle_game_configuration(self) -> None:
        self.workshop_items_dict = self.game_utils.handle_configuration(
            config=self.config, steam_client=self.steam_client
        )

    def launch(self) -> None:
        self.game_utils.launch()
