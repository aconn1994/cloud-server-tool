:: Remove entities to be replaced
:: docker container rm a3-server
:: docker rmi $(docker images 'arma-server' -q)
:: rmdir /q /s dist

:: Setup build directory with entities
mkdir dist
cd lib/python/arma3
tar -cvzf server_config.tar.gz *
XCOPY /i /y C:\Users\Chris\Documents\adams_arma\cloud-server-tool\lib\python\arma3\server_config.tar.gz C:\Users\Chris\Documents\adams_arma\cloud-server-tool\dist\
rm server_config.tar.gz
cd ../../..
XCOPY /i /y C:\Users\Chris\Documents\adams_arma\cloud-server-tool\requirements.txt C:\Users\Adam\dev\cloud-server-tool\dist\

:: Rebuild docker image and run
docker build -t arma-server:latest .
docker image prune -f
docker volume prune -f
docker run --name a3-server -p 2302:2302/udp -p 2303:2303/udp -p 2304:2304/udp -p 2305:2305/udp -p 2306:2306/udp -it arma-server
