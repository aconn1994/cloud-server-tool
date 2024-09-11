#!/usr/bin/python3

import os
import SteamClient.SteamCMDClient as SCC

def main():

    # Environment Variables (DockerFile)
    STEAMCMD_DIR = os.path.join(os.getcwd(), os.environ['DIR_STEAMCMD'])
    LOCAL_GAME_DIR = os.path.join(STEAMCMD_DIR, os.environ['DIR_LOCAL_GAME'])
    LOCAL_MOD_DIR = os.path.join(LOCAL_GAME_DIR, os.environ['DIR_LOCAL_MOD'])
    LOCAL_KEYS_DIR = os.path.join(LOCAL_GAME_DIR, os.environ['DIR_KEYS_DIR'])
    STEAM_DOWNLOAD_DIR = os.path.join(LOCAL_GAME_DIR, os.environ['DIR_STEAM_MOD_DOWNLOAD'])
    STEAM_USERNAME = os.environ['STEAM_USERNAME']
    STEAM_PASSWORD = os.environ['STEAM_PASSWORD']
    GAME_SERVER_ID = os.environ['GAME_SERVER_ID']
    GAME_WORKSHOP_ID = os.environ['GAME_WORKSHOP_ID']
    
    print(STEAMCMD_DIR)
    print(LOCAL_GAME_DIR)
    print(LOCAL_MOD_DIR)
    print(LOCAL_KEYS_DIR)
    print(STEAM_DOWNLOAD_DIR)
    print(STEAM_USERNAME)
    print(STEAM_PASSWORD)
    print(GAME_SERVER_ID)
    print(GAME_WORKSHOP_ID)

    steam_client = SCC.SteamCMDClient(
        LOCAL_GAME_DIR,
        STEAM_DOWNLOAD_DIR,
        STEAM_USERNAME,
        STEAM_PASSWORD
    )

    steam_client.install_game(GAME_SERVER_ID)


if __name__ == '__main__':
    main()
