import argparse
from clients.DockerClient import DockerClient

parser = argparse.ArgumentParser()
parser.add_argument(
    "-c", "--clean-up", help="Clean up local docker entities", action="store_true"
)


def main():
    args = parser.parse_args()
    workspace = "game-server"
    docker = DockerClient(workspace, exists=args.clean_up)

    if args.clean_up:
        docker.remove_container(force=True)
        docker.remove_image(force=True)
        docker.prune("container", force=True)
        docker.prune("image", force=True)
        docker.prune("volume", force=True)

    docker.build_image()


if __name__ == "__main__":
    main()
