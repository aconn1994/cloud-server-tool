from html.parser import HTMLParser
import os
import re
import subprocess
from typing import Any


def format_name(name: str):
    return re.sub("[^A-Za-z0-9]+", "", name)


class ArmaThreeHTMLParser(HTMLParser):  # TO BE CONTINUED.............
    def __init__(self):
        super(ArmaThreeHTMLParser, self).__init__()
        self.html_as_dict: dict[str, str] = {}
        self.start_tag: str = None
        self.is_display_name: str = False
        self.display_name: str = None

    def handle_starttag(self, tag: str, attrs: list[tuple]):
        if tag == "td":
            for attr in attrs:
                if attr[0] == "data-type" and attr[1] == "DisplayName":
                    self.start_tag = tag
                    self.is_display_name = True
        elif tag == "a":
            self.start_tag = tag

    def handle_data(self, data: str):
        if self.start_tag == "td" and self.is_display_name:
            self.display_name = format_name(data)
            self.html_as_dict[self.display_name] = None
            self.is_display_name = False
        elif self.start_tag == "a" and self.display_name:
            self.html_as_dict[self.display_name] = data.split("=")[1]
            self.display_name = None


def get_configuration(
    local_game_dir: str,
    game_install_dir: str,
) -> dict[str, str]:  # Convert to Python Model/Yaml File pattern?
    return {
        "game_id": "233780",
        "workshop_id": "107410",
        "binary": "arma3server_x64",
        "game_install_dir": game_install_dir,
        "mod_file_path": os.path.join("cst_game", local_game_dir, "mod-list.html"),
        "mod_dir": os.path.join(game_install_dir, "mods"),
        "keys_dir": os.path.join(game_install_dir, "keys"),
        "configuration_file_path": os.path.join(local_game_dir, "server.cfg"),
        "workshop_download_path": os.path.join(
            game_install_dir, "steamapps", "workshop", "content"
        ),
    }


def parse_mod_file(mod_file_path: str) -> dict[str, str]:
    html_parser = ArmaThreeHTMLParser()
    mf = open(mod_file_path, "r")
    html_parser.feed(mf.read())
    return html_parser.html_as_dict


def handle_configuration(config: dict[str, str], steam_client: Any) -> dict[str, str]:
    configuration_file_path = config["configuration_file_path"]
    game_install_dir = config["game_install_dir"]
    workshop_id = config["workshop_id"]
    mod_dir = config["mod_dir"]
    keys_dir = config["keys_dir"]
    workshop_download_path = config["workshop_download_path"]
    workshop_dict = parse_mod_file(config["mod_file_path"])

    if os.path.exists(os.path.join(game_install_dir, "server.cfg")):
        os.remove(os.path.join(game_install_dir, "server.cfg"))
    os.symlink(os.path.join(os.getcwd(), "cst_game", configuration_file_path), os.path.join(game_install_dir, "server.cfg"))

    for workshop_item_name, workshop_item_id in workshop_dict.items():
        if not os.path.exists(mod_dir):
            os.makedirs(mod_dir)

        steam_client.download_workshop_mod(workshop_id, workshop_item_id)
        steam_workshop_download_path = os.path.join(
            workshop_download_path, workshop_id, workshop_item_id
        )
        steam_workshop_keys_path = os.path.join(steam_workshop_download_path, "keys")
        workshop_item_key_name = os.listdir(steam_workshop_keys_path)[0]
        try:
            os.symlink(
                steam_workshop_download_path,
                os.path.join(mod_dir, f"@{workshop_item_name}"),
            )
        except FileExistsError:
            print("Mod already Linked")

        try:
            os.symlink(
                os.path.join(steam_workshop_keys_path, workshop_item_key_name),
                os.path.join(keys_dir, workshop_item_key_name),
            )
        except FileExistsError:
            print("Key Already Linked")

    return workshop_dict


def launch(config: dict[str, str], workshop_item_names: list[str]) -> None:
    os.chdir(config["game_install_dir"])
    launch_cmd = ["./" + config["binary"]]
    launch_cmd.extend(["-name=server"])
    for workshop_item_name in workshop_item_names:
        launch_cmd.extend([f"-mod=mods/@{workshop_item_name}"])

    launch_cmd.extend(["-config=server.cfg"])

    print(" ".join(launch_cmd))
    subprocess.call(launch_cmd)

