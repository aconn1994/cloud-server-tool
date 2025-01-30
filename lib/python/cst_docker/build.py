from DockerClient import DockerClient

def main():
    docker = DockerClient()
    game_image = docker.get_image('game-server')
    print(game_image)

if __name__ == '__main__':
    main()