import os
import subprocess


class SteamCMDClient:
    def __init__(
        self,
        local_game_dir: str,
        username: str | None = None,
        password: str | None = None,
    ):
        self.local_game_dir: str = local_game_dir
        self._username: str | None = username or os.environ.get("STEAM_USERNAME")
        self._password: str | None = password or os.environ.get("STEAM_PASSWORD")

    @property
    def has_credentials(self) -> bool:
        return self._username is not None and self._password is not None

    def install_game(self, game_id: str, beta_arg: str | None = None) -> None:
        steamcmd = ["./steamcmd/steamcmd.sh"]
        steamcmd.extend(["+force_install_dir", self.local_game_dir])

        if self._username is not None and self._password is not None:
            steamcmd.extend(["+login", self._username, self._password])
        else:
            print("Steam Username and/or Password not provided. Logging in anonymously...")
            steamcmd.extend(
                ["+login", "anonymous"]
            )  # todo, certain games cannot be downloaded anonymously

        steamcmd.extend(["+app_update", game_id])

        if beta_arg:
            steamcmd.extend(["-beta", beta_arg])

        steamcmd.extend(["validate", "+quit"])
        subprocess.call(steamcmd)

    def download_workshop_mod(self, game_workshop_id: str, workshop_item_id: str) -> None:
        steamcmd = ["./steamcmd/steamcmd.sh"]
        steamcmd.extend(["+force_install_dir", self.local_game_dir])

        if self._username is not None and self._password is not None:
            steamcmd.extend(["+login", self._username, self._password])
        else:
            print(
                "Steam Username and Password required to download workshop items. Trying to download workshop items anonymously..."
            )
            steamcmd.extend(["+login", "anonymous"])

        steamcmd.extend(["+workshop_download_item", game_workshop_id, workshop_item_id, "validate"])
        steamcmd.extend(["+quit"])

        subprocess.call(steamcmd)

    def launch_server(self) -> None:
        pass
