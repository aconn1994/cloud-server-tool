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


def main():
    args = parser.parse_args()
    ports = args.ports
    steam_username = args.steam_username
    steam_password = args.steam_password
    workspace = "game-server"
    clean_up = args.clean_up
    local_game_installer_path = (
        "/Users/adamconnolly/dev/cloud-server-tool/lib/python/cst"
    )
    container_game_installer_path = "/home/gameuser/cst_game"
    docker = DockerClient(workspace_name=workspace, exists=clean_up)

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
        local_game_installer_path=local_game_installer_path,
        container_game_installer_path=container_game_installer_path,
        interactive_shell=True,
    )


if __name__ == "__main__":
    main()
