import argparse
import logging
from clients.DockerClient import DockerClient

parser = argparse.ArgumentParser()
parser.add_argument(
    "-c", "--clean-up", help="Clean up local docker entities", action="store_true"
)
parser.add_argument("--ports", "-ps", help="ports", required=True)
parser.add_argument(
    "--steam-username", "-su", help="Steam username", required=True, default=None
)
parser.add_argument(
    "--steam-password", "-sp", help="Steam password", required=True, default=None
)
parser.add_argument("--debug", help="Debug mode", action="store_true")


def main():
    args = parser.parse_args()
    debug_mode = args.debug
    ports = args.ports
    steam_username = args.steam_username
    steam_password = args.steam_password
    workspace = "game-server"
    clean_up = args.clean_up
    local_game_installer_path = (
        "/Users/adamconnolly/dev/cloud-server-tool/lib/python/cst"
    )
    container_game_installer_path = "/home/gameuser/cst_game"
    logger = logging.getLogger(__name__)

    if debug_mode:
        logging.basicConfig(level=logging.DEBUG)

    docker = DockerClient(workspace_name=workspace, exists=clean_up, logger=logger)

    if args.clean_up:
        logger.debug("Cleaning up local docker entities...")
        docker.remove_container(force=True)
        docker.remove_image(force=True)
        docker.prune("container", force=True, logger=logger)
        docker.prune("image", force=True, logger=logger)
        docker.prune("volume", force=True, logger=logger)
        logger.debug("Cleaned up local docker entities.")

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
