from abc import ABC
from typing import Any

from cst_game.common.abstract_game_setup import AbstractGameSetup
from cst_game.common.game_setup_runner_args import GameSetupRunnerArgs
from cst_game.games.arma_three.game_config import GameConfig


class Setup(AbstractGameSetup, ABC):
    def __init__(self, parsed_args: GameSetupRunnerArgs) -> None:
        super().__init__(parsed_args=parsed_args)
        self.game_config = GameConfig(self.parsed_args.operating_system)
        self.os_manager = self.game_config.os_manager
        self.logger = self.init_logger()

    def name(self) -> str:
        return "Arma 3 Game Server Setup"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        self.logger.debug(f"Executing {self.name()}...")
        self.logger.debug(f"{self.name()} has been Executed.")


def main(parsed_args: GameSetupRunnerArgs) -> None:
    Setup(parsed_args=parsed_args).execute()
