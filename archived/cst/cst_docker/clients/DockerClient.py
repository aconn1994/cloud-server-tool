import os
import subprocess


class DockerClient:
    def __init__(self, workspace_name: str, exists: bool = False):
        self.workspace_name: str = workspace_name
        self.exists: bool = exists

        self.container_id: str | None = None
        self.image_id: str | None = None

        if exists:
            self._get_container_id()
            self._get_image_id()

    def _get_container_id(self) -> None:
        docker_cmd = ["docker"]
        docker_cmd.extend(["ps", "-aqf", f"name={self.workspace_name}"])
        self.container_id = subprocess.run(
            docker_cmd, capture_output=True, text=True
        ).stdout.strip()

    def _get_image_id(self) -> None:
        docker_cmd = ["docker"]
        docker_cmd.extend(["images", "-q", self.workspace_name])
        self.image_id = subprocess.run(
            docker_cmd, capture_output=True, text=True
        ).stdout.strip()

    def remove_container(self, force: bool = False) -> None:
        docker_cmd = ["docker"]
        docker_cmd.extend(["container", "rm", self.container_id])
        if force:
            docker_cmd.extend("--force")

    def remove_image(self, force: bool = False) -> None:
        docker_cmd = ["docker"]
        docker_cmd.extend(["rmi", self.image_id])
        if force:
            docker_cmd.extend("--force")
        subprocess.call(docker_cmd)

    @staticmethod
    def prune(
        entity_type: str,
        all_entities: bool = False,
        force: bool = False,
    ) -> None:
        docker_cmd = ["docker"]
        docker_cmd.extend([entity_type, "prune"])
        if all_entities:
            docker_cmd.extend(["-a"])
        if force:
            docker_cmd.extend(["-f"])
        subprocess.call(docker_cmd)

    def build_image(
        self,
        ports: str,
        steam_username: str,
        steam_password: str,
        local_game_installer_path: str,
    ) -> None:
        docker_cmd = ["docker"]
        docker_cmd.extend(["build", "-t", f"{self.workspace_name}:latest"])

        if ports:
            docker_cmd.extend(["--build-arg", f"PORTS={ports}"])
        if steam_username and steam_password:
            docker_cmd.extend(
                [
                    "--build-arg",
                    f"STEAM_USERNAME_ARG={steam_username}",
                    "--build-arg",
                    f"STEAM_PASSWORD_ARG={steam_password}",
                ]
            )
        docker_cmd.extend([f"{local_game_installer_path}/cst_docker"])
        subprocess.call(docker_cmd)

    def run_image_as_container(
        self,
        ports: str,
        container_game_installer_path: str,
        interactive_shell: bool = False,
    ):
        docker_cmd = ["docker"]
        docker_cmd.extend(["run", "--name", self.workspace_name])

        for port in ports.split(" "):
            docker_cmd.extend(["-p", f"{port.split('/')[0]}:{port}"])

        docker_cmd.extend(
            [
                "-v",
                f"{os.getcwd()}/dist:{container_game_installer_path}",
            ]
        )

        if interactive_shell:
            docker_cmd.extend(["-it"])

        docker_cmd.extend([self.workspace_name])
        subprocess.call(docker_cmd)
