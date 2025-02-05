#!/bin/bash

set -euo pipefail

docker rm -f cst-base-container
docker compose up -d cst-debug