from typing import Any

from arma_three.arma_three_util import ArmaThreeUtil


class GameConfig:
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
        self.game_utils: Any | None = None
        self.game_id: str | None = None

        self.game_utils_mapper = {
            "arma_three_util": ArmaThreeUtil,
        }

    def execute(self) -> None:
        self.game_utils = self.game_utils_mapper[f"{self.local_game_dir}_util"](
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
