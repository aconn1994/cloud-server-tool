#!/bin/bash

set -euo pipefail

# CICD
#/bin/bash .cicd/bash/testers/coverage-pytest.sh .cicd/python .cicd/python cst_cicd pyproject.toml /usr/local/bin/python3

# cst
/bin/bash .cicd/bash/testers/coverage-pytest.sh lib/python/cst lib/python/cst cst pyproject.toml /root/venvs/cst/bin/python3

