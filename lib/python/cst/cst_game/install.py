import os
from clients.SteamCMDClient import SteamCMDClient
from clients.GameConfigClient import GameConfigClient
from utils import Utils


def main():
    steamcmd_dir: str = os.path.join(os.getcwd(), "steamcmd")
    local_game_dir: str = os.environ["LOCAL_GAME_DIR"]
    steam_username: str = os.environ["STEAM_USERNAME"]
    steam_password: str = os.environ["STEAM_PASSWORD"]
    local_game_assets_dir: str = os.path.join(os.getcwd(), "cst_game", local_game_dir)
    game_install_dir: str = os.path.join(steamcmd_dir, local_game_dir)

    steam_client = SteamCMDClient(local_game_dir, steam_username, steam_password)
    utils = Utils()
    gc_client = GameConfigClient(
        local_game_dir=local_game_dir,
        local_game_assets_dir=local_game_assets_dir,
        game_install_dir=game_install_dir,
        steam_client=steam_client,
        utils=utils,
    )
    gc_client.execute()
    game_id = gc_client.game_id

    steam_client.install_game(game_id)
    gc_client.handle_game_configuration()
    # gc_client.launch()


if __name__ == "__main__":
    main()
