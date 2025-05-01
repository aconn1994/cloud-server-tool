from typing import Any

from cst_game.common.abstract_game_setup import AbstractGameSetup


class DummySetup(AbstractGameSetup):
    def __init__(self):
        super().__init__(parsed_args=None)  # type: ignore
        self.dummy_variable = "dummy_value"

    @property
    def name(self) -> str:
        return "Dummy Setup Name"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        print(f"Printing dummy variable value: {self.dummy_variable}")


def test_abstract_game_setup() -> None:
    dummy_setup = DummySetup()
    dummy_setup.execute()

    assert dummy_setup.name == "Dummy Setup Name"
    assert dummy_setup.dummy_variable == "dummy_value"
