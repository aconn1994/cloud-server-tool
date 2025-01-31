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
        docker_cmd = ['docker']
        docker_cmd.extend(['ps', '-aqf', f'name={self.workspace_name}'])
        self.container_id = subprocess.run(docker_cmd, capture_output=True, text=True).stdout.strip()

    def _get_image_id(self) -> None:
        docker_cmd = ['docker']
        docker_cmd.extend(['images', '-q', self.workspace_name])
        self.image_id = subprocess.run(docker_cmd, capture_output=True, text=True).stdout.strip()

    def remove_container(self, force: bool = False) -> None:
        print(f'Cleaning up {self.workspace_name} container...')
        docker_cmd = ['docker']
        docker_cmd.extend(['container', 'rm', self.container_id])
        if force:
            docker_cmd.extend('--force')
        print(f'{self.workspace_name} container has been removed.')

    def remove_image(self, force: bool = False) -> None:
        print(f'Cleaning up {self.workspace_name} image...')
        docker_cmd = ['docker']
        docker_cmd.extend(['rmi', self.image_id])
        if force:
            docker_cmd.extend('--force')
        subprocess.call(docker_cmd)
        print(f'{self.workspace_name} image has been removed.')

    @staticmethod
    def prune(entity_type: str, all_entities: bool = False, force: bool = False) -> None:
        docker_cmd = ['docker']
        docker_cmd.extend([entity_type, 'prune'])
        if all_entities:
            docker_cmd.extend(['-a'])
        if force:
            docker_cmd.extend(['-f'])
        subprocess.call(docker_cmd)

    def build_image(self) -> None:
        # todo, use yaml as config???
        pass