# cloud-server-tool
Tool for deploying steam game servers in AWS.

## Run Arma 3
python3 lib/python/cst/cst_docker/build.py --ports "2302/udp 2303/udp 2304/udp 2305/udp 2306/udp" --steam-username=<your-steam-username> --steam-password=<your-steam-password>
