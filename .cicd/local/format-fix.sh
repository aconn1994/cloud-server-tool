#!/bin/bash

set -euo pipefail

# CICD
/bin/bash .cicd/bash/linters/python-format.sh .cicd/python .cicd/python cicd "" .cicd/python/pyproject.toml /root/venvs/cicd/bin/python3

# CST
#/bin/bash .cicd/bash/linters/python-format.sh .cicd/python lib/python/cst cst "" lib/python/cst/pyproject.toml /root/venvs/cst/bin/python3

# cst
/bin/bash .cicd/bash/linters/python-format.sh lib/python/cst lib/python/cst cst "" lib/python/cst/pyproject.toml /root/venvs/cst/bin/python3