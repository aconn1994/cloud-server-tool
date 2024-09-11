#!/bin/bash
# Wrapper file to start the A3 server

# Server Name
server=server

# Server mods
mods=

# Config File Name
config=server.cfg

# Start Server
./arma3server_x64 -name=$server $mods -config=$config
