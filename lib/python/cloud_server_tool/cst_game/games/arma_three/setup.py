from abc import ABC
from typing import Any

from cst_game.common.abstract_game_setup import AbstractGameSetup
from cst_game.common.game_setup_runner_args import GameSetupRunnerArgs


class Setup(AbstractGameSetup, ABC):
    def __init__(self, parsed_args: GameSetupRunnerArgs) -> None:
        super().__init__(parsed_args=parsed_args)

    def name(self) -> str:
        return "Arma Three Game Server Setup"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        pass


def main(parsed_args: GameSetupRunnerArgs) -> None:
    Setup(parsed_args=parsed_args).execute()
