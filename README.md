# cloud-server-tool
Tool for deploying steam game servers in AWS.

## Package /lib/python/arma3 directory for shipping to image
`xcopy C:\Users\Adam\dev\cloud-server-tool\lib\python\arma3 C:\Users\Adam\dev\cloud-server-tool\dist\arma3 /e /y /i`

## Build Container Image
`docker build -t arma-server:latest .`

## Create Container Locally For Testing
`docker run --name a3-server -it arma-server`