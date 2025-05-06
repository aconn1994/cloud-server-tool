import os
from typing import Any

from cst_game.common.abstract_game_setup import AbstractGameSetup
from cst_game.games.arma_three.arma_three_html_parser import ArmaThreeHTMLParser


class DummyArmaThreeSetup(AbstractGameSetup):
    def __init__(self):
        super().__init__(parsed_args=None)  # type: ignore
        self.dummy_variable = "dummy_value"

    @property
    def name(self) -> str:
        return "Dummy Setup Name"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        print(f"Printing dummy variable value: {self.dummy_variable}")


def test_arma_three_html_parser() -> None:
    mock_mod_list_path = os.path.join("mock_data", "mock-mod-list.html")

    dummy_arma_three_setup = DummyArmaThreeSetup()
    dummy_arma_three_setup.execute()
    assert dummy_arma_three_setup.name == "Dummy Setup Name"

    arma_three_html_parser = ArmaThreeHTMLParser(dummy_arma_three_setup.reformat_string)

    if os.path.exists(mock_mod_list_path):
        mf = open(mock_mod_list_path, "r")
        arma_three_html_parser.feed(mf.read())
        workshop_items = arma_three_html_parser.html_as_dict
        assert type(workshop_items) is dict
        assert len(workshop_items) == 17
        assert workshop_items["CBAA3"] == "450814997"
        assert workshop_items["DUISquadRadar"] == "1638341685"
        assert workshop_items["EnhancedMovement"] == "333310405"
        assert workshop_items["EnhancedMovementRework"] == "2034363662"
