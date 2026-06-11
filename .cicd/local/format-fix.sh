#!/bin/bash

set -euo pipefail

# CICD
/bin/bash .cicd/bash/linters/python-format.sh .cicd/python .cicd/python cicd "" .cicd/python/pyproject.toml /root/venvs/cicd/bin/python3

# CST
#/bin/bash .cicd/bash/linters/python-format.sh .cicd/python lib/python/cst cst "" lib/python/cst/pyproject.toml /root/venvs/cst/bin/python3

# cloud-server-tool
/bin/bash .cicd/bash/linters/python-format.sh lib/python/cloud-server-tool lib/python/cloud-server-tool cloud-server-tool "" lib/python/cloud-server-tool/pyproject.toml /root/venvs/cloud-server-tool/bin/python3