# Remove entities to be replaced
docker container rm a3-server
docker rmi $(docker images 'arma-server' -q)
# rm -rf dist

# # Setup build directory with entities
# mkdir dist
# cd lib/python
# tar -cvzf server_config.tar.gz *
# cd ../..
# cp lib/python/server_config.tar.gz dist/server_config.tar.gz
# rm lib/python/server_config.tar.gz

# Rebuild docker image and run
docker image prune -f
docker volume prune -f
docker build -t arma-server:latest .
docker run --name a3-server -p 2302:2302/udp -p 2303:2303/udp -p 2304:2304/udp -p 2305:2305/udp -p 2306:2306/udp -v ./lib/python:/home/gameuser -it arma-server
