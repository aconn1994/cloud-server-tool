import subprocess

class SteamCMDClient:
    def __init__(self,
        local_game_dir,
        steam_download_dir,
        username,
        password
    ):
        self.local_game_dir: str = local_game_dir
        self.steam_download_dir: str = steam_download_dir
        self._username: str = username
        self._password: str = password
    
    def install_game(self, game_id: str) -> None:
        steamcmd = ['./steamcmd/steamcmd.sh']
        steamcmd.extend(['+force_install_dir', self.local_game_dir])

        if self._username != 'NULL' and self._password != 'NULL':
            steamcmd.extend(['+login', self._username, self._password])
        else:
            print('Steam Username and/or Password not provided. Logging in anonymously...')
            steamcmd.extend(['+login', 'anonymous'])

        steamcmd.extend(['+app_update', game_id, 'validate'])
        steamcmd.extend(['+quit'])

        subprocess.call(steamcmd)

    def download_workshop_mod(self, game_id: str, game_workshop_id: str) -> None:
        steamcmd = ['./steamcmd/steamcmd.sh']

        if self._username != 'NULL' and self._password != 'NULL':
            steamcmd.extend(['+login', self._username, self._password])
        else:
            print('Steam Username and Password required to download workshop items. Trying to download workshop items anonymously...')
            steamcmd.extend(['+login', 'anonymous'])
        
        steamcmd.extend('+workshop_download_item', game_id, game_workshop_id, 'validate')
        steamcmd.extend(['+quit'])

        subprocess.call(steamcmd)
    
    def launch_server(self):
        pass

