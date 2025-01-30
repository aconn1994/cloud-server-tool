# Remove entities to be replaced
docker container rm game-server
docker rmi $(docker images 'game-server' -q)

# Rebuild docker image and run
docker image prune -f
docker volume prune -f
docker build -t game-server:latest --build-arg STEAM_USERNAME_ARG=$1 --build-arg STEAM_PASSWORD_ARG=$2 .
docker run --name game-server -p 2302:2302/udp -p 2303:2303/udp -p 2304:2304/udp -p 2305:2305/udp -p 2306:2306/udp -v /Users/adamconnolly/dev/cloud-server-tool/lib/python/cst_game:/home/gameuser/cst_game -it game-server
