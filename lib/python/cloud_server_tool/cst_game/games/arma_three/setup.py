import os
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
        self.game_install_dir = os.path.join(
                self.os_manager.instance_root_dir,
                "steamcmd",
                self.game_config.game_name,
            )
        self.steam_cmd_client = self.game_config.steam_client(self.game_install_dir)

    def name(self) -> str:
        return "Arma 3 Game Server Setup"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        self.logger.warning(f"Executing {self.name()}...")

        self.game_config.install_steamcmd_binary()  # Install SteamCMD

        if not os.path.exists(self.game_install_dir):
            os.mkdir(self.game_install_dir)

        self.steam_cmd_client.install_game(self.game_config.game_id)

        self.logger.warning(f"{self.name()} has been Executed.")


def main(parsed_args: GameSetupRunnerArgs) -> None:
    Setup(parsed_args=parsed_args).execute()
