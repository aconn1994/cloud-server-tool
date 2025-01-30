import subprocess

class DockerClient:
    def __init__(self):
        self.docker_binary = ['docker']

    def help(self) -> None:
        docker_cmd = self.docker_binary
        docker_cmd.extend(['--help'])
        subprocess.call(docker_cmd)

    def get_image(self, game_image_name: str) -> str:
        docker_cmd = self.docker_binary
        docker_cmd.extend(['images', '-q', game_image_name])
        return subprocess.run(docker_cmd, capture_output=True, text=True).stdout.strip()


    def remove_game_image(self):
        docker_cmd = self.docker_binary
        docker_cmd.extend(['rmi', "$(docker images 'game-server' -q)"])

        subprocess.check_call(docker_cmd)
        subprocess.call(docker_cmd)