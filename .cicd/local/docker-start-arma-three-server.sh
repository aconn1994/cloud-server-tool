#!/bin/bash

set -euo pipefail

docker rm -f arma-three-server-container
docker compose up -d arma-three-server