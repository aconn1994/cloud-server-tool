import subprocess

class SteamCMDClient:
    def __init__(self,
        local_game_dir,
        steam_download_dir,
        username,
        password
    ):
        self.local_game_dir = local_game_dir
        self.steam_download_dir = steam_download_dir
        self._username = username
        self._password = password
    
    def install_game(self, game_id):
        steamcmd = ['./steamcmd/steamcmd.sh']
        steamcmd.extend(['+force_install_dir', self.local_game_dir])

        if self._username and self._password:
            steamcmd.extend(['+login', self._username, self._password])
        else:
            print("Steam Username and/or Password not provided. Logging in anonymously...")
            steamcmd.extend(['+login', 'anonymous'])

        steamcmd.extend(['+app_update', game_id, 'validate'])
        steamcmd.extend(['+quit'])

        subprocess.call(steamcmd)

    def download_workshop_mod(self, game_id, game_workshop_id): # Install one mod at a time... or make object with all mod information??
        steamcmd = ['./steamcmd/steamcmd.sh']

        if self._username and self._password:
            steamcmd.extend(['+login', self._username, self._password])

        else:
            print("Steam Username and Password required to download workshop items. Skipping workshop downloads...")
            

