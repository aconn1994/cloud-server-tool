#!/bin/bash

set -euo pipefail

# CICD
#/bin/bash .cicd/bash/testers/coverage-pytest.sh .cicd/python .cicd/python cst_cicd pyproject.toml python3 # todo, need to fix

# cloud-server-tool
/bin/bash .cicd/bash/testers/coverage-pytest.sh lib/python/cloud-server-tool lib/python/cloud-server-tool cloud-server-tool pyproject.toml /root/venvs/cloud-server-tool/bin/python3

