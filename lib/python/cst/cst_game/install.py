import os
from clients.SteamCMDClient import SteamCMDClient
from clients.GameConfigClient import GameConfigClient


def main():

    # Environment Variables (DockerFile)
    steamcmd_dir: str = os.path.join(os.getcwd(), os.environ['DIR_STEAMCMD'])
    local_game_id: str = os.environ['DIR_LOCAL_GAME']
    local_game_dir: str = os.path.join(steamcmd_dir, local_game_id)
    local_mod_dir: str = os.path.join(local_game_dir, os.environ['DIR_LOCAL_MOD'])
    local_keys_dir: str = os.path.join(local_game_dir, os.environ['DIR_KEYS_DIR'])
    steam_username: str = os.environ['STEAM_USERNAME']
    steam_password: str = os.environ['STEAM_PASSWORD']
    game_server_id: str = os.environ['GAME_SERVER_ID']
    game_workshop_id: str = os.environ['GAME_WORKSHOP_ID']
    steam_download_dir: str = os.path.join(local_game_dir, os.environ['DIR_STEAM_MOD_DOWNLOAD'], game_workshop_id)

    
    print(steamcmd_dir)
    print(local_game_id)
    print(local_game_dir)
    print(local_mod_dir)
    print(local_keys_dir)
    print(steam_download_dir)
    print(steam_username)
    print(steam_password)
    print(game_server_id)
    print(game_workshop_id)

    gc_client = GameConfigClient(local_game_id) ## NEEDS PROPER TESTING
    steam_client = SteamCMDClient(
        local_game_dir,
        steam_download_dir,
        steam_username,
        steam_password
    )


    steam_client.install_game(game_server_id)

    if gc_client.workshop_items_dict:
        gc_client.handle_mod_configuration(
            steam_client,
            game_server_id,
            local_game_dir,
            local_mod_dir,
            steam_download_dir
        )

if __name__ == '__main__':
    main()
