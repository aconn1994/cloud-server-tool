#!/bin/bash

set -euo pipefail

# CICD
#/bin/bash .cicd/bash/testers/coverage-pytest.sh .cicd/python/cst_cicd .cicd/python/cst_cicd cst_cicd pyproject.toml python3 # todo, need to fix

# cloud_server_tool
/bin/bash .cicd/bash/testers/coverage-pytest.sh lib/python/cloud_server_tool lib/python/cloud_server_tool cloud_server_tool pyproject.toml /root/venvs/cloud_server_tool/bin/python3

