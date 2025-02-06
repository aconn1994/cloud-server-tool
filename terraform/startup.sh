#!/bin/bash
sudo apt update -y
sudo apt-get install -y docker.io git python3

cd /home/ubuntu
git clone https://github.com/aconn1994/cloud-server-tool.git
cd lib/python/cst/cst_docker
python3 build.py