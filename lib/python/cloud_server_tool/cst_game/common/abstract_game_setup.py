from abc import ABC, abstractmethod

from cst_game.common.game_setup_runner_args import GameSetupRunnerArgs


class AbstractGameSetup(ABC):
    def __init__(self, parsed_args: GameSetupRunnerArgs) -> None:
        self.parsed_args = parsed_args

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def _initialize(self) -> None:
        pass
