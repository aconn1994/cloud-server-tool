import logging

from cst_game.common.game_setup_runner_parser import parse_and_run
from cst_game.games.arma_three.game_config import GameConfig

MODULE_NAME = "tests.common.module_for_test_game_setup_runner_parser"
OPERATING_SYSTEM = "linux"
base_args = ["--module-name", MODULE_NAME, "--operating-system", OPERATING_SYSTEM]

logger = logging.getLogger(__name__)


def test_game_config() -> None:
    game_config = GameConfig(parsed_args=parse_and_run(supplied_args=base_args), logger=logger)
    os_manager = game_config.os_manager

    assert game_config.game_id == "233780"
    assert game_config.game_workshop_id == "107410"
    assert game_config.binary_32bit == "arma3server_x32"
    assert game_config.binary_64bit == "arma3server_x64"
    assert game_config.username is None
    assert game_config.password is None
    assert os_manager.operating_system_alias == "linux"
    assert os_manager.instance_root_dir == f"/home/{game_config.os_manager.default_game_folder}"
