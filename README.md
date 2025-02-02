# cloud-server-tool
Tool for deploying steam game servers in AWS.

## Package /lib/python/arma3 directory for shipping to image
`xcopy C:\Users\Adam\dev\cloud-server-tool\lib\python\arma3 C:\Users\Adam\dev\cloud-server-tool\dist\arma3 /e /y /i`

## Build Container Image
`docker build -t arma-server:latest .`

## Create Container Locally For Testing
`docker run --name a3-server -p 2302:2302/udp -p 2303:2303/udp -p 2304:2304/udp -p 2305:2305/udp -p 2306:2306/udp -it arma-server`

## Todos:
- Create CICD directory
  - Use pylint for formatting and error checking
  - Pytest for module unit testing, lots of asserts
- Setup local interpreter with docker and game code as separate modules using docker
- Use yaml as interface for generating server instances
  - Possibly tracking needed files and utils for deployment and runtime