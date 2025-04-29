import os
import shutil
import argparse
from clients.DockerClient import DockerClient

parser = argparse.ArgumentParser()
parser.add_argument(
    "-c", "--clean-up", help="Clean up local docker entities", action="store_true"
)
parser.add_argument(
    "-bi", "--build-image", help="Build docker image", action="store_true"
)
parser.add_argument("--ports", "-ps", help="ports", required=True)
parser.add_argument(
    "--steam-username", "-su", help="Steam username", required=True, default=None
)
parser.add_argument(
    "--steam-password", "-sp", help="Steam password", required=True, default=None
)
parser.add_argument("--game-name", "-gn", help="Game Name", required=True)


def prep_cst_game_dist_folder(
    local_game_installer_path: str,
    game_name: str,
):
    dist_directory = os.path.join(os.getcwd(), "dist")
    shutil.copytree(os.path.join(local_game_installer_path, "cst_game"), dist_directory)
    shutil.rmtree(os.path.join(dist_directory, "game_assets"))
    shutil.copytree(
        os.path.join(local_game_installer_path, "game_assets", game_name),
        os.path.join(dist_directory, "game_assets"),
    )


def main():
    args = parser.parse_args()
    ports = args.ports
    steam_username = args.steam_username
    steam_password = args.steam_password
    game_name = args.game_name
    workspace = "game-server"
    clean_up = args.clean_up
    local_game_installer_path = os.path.join(os.getcwd(), "lib", "python", "cst")
    container_game_installer_path = "/home/gameuser/cst_game"
    docker = DockerClient(workspace_name=workspace, exists=clean_up)

    prep_cst_game_dist_folder(
        local_game_installer_path=local_game_installer_path,
        game_name=game_name,
    )

    if args.clean_up:
        docker.remove_container(force=True)
        docker.remove_image(force=True)
        docker.prune("container", force=True)
        docker.prune("image", force=True)
        docker.prune("volume", force=True)

    if args.build_image:
        docker.build_image(
            ports=ports,
            steam_username=steam_username,
            steam_password=steam_password,
            local_game_installer_path=local_game_installer_path,
        )

    docker.run_image_as_container(
        ports=ports,
        container_game_installer_path=container_game_installer_path,
        interactive_shell=True,
    )

    shutil.rmtree(os.path.join(os.getcwd(), "dist"))


if __name__ == "__main__":
    main()
