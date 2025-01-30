:: Remove entities to be replaced
docker container rm game-server
docker rmi $(docker images 'game-server' -q)
:: rmdir /q /s dist

:: Setup build directory with entities
:: mkdir dist
:: cd lib/python
:: tar -cvzf server_config.tar.gz *
:: XCOPY /i /y C:\Users\Adam\dev\cloud-server-tool\lib\python\server_config.tar.gz C:\Users\Adam\dev\cloud-server-tool\dist\
:: del server_config.tar.gz
:: cd ../..

:: Rebuild docker image and run
docker build -t game-server:latest .
docker image prune -f
docker volume prune -f
docker run --name game-server -p 2302:2302/udp -p 2303:2303/udp -p 2304:2304/udp -p 2305:2305/udp -p 2306:2306/udp -v C:/Users/Adam/dev/cloud-server-tool/lib/python/cst_game:/home/gameuser -it game-server
