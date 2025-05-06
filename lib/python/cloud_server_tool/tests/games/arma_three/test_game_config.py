import getpass

from cst_game.games.arma_three.game_config import GameConfig


def test_game_config() -> None:
    game_config = GameConfig(operating_system="linux")
    os_manager = game_config.os_manager

    assert game_config.game_id == "233780"
    assert game_config.game_workshop_id == "107410"
    assert game_config.binary_32bit == "arma3server_x32"
    assert game_config.binary_64bit == "arma3server_x64"
    assert game_config.username is None
    assert game_config.password is None
    assert os_manager.operating_system_alias == "linux"
    assert os_manager.instance_root_dir == f"/home/{getpass.getuser()}"
