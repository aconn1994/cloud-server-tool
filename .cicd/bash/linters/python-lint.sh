#!/bin/bash

set -eo pipefail

PYTHONPATH=$1
MODULE=$2
LOG_ALIAS=$3
PYPROJECT_TOML_PATH=$4
PYTHON_INTERPRETER=$5

export PYTHONPATH
echo "PYTHONPATH is set to ${PYTHONPATH}"
echo "Linting ${MODULE}"

set +e

# ruff
$PYTHON_INTERPRETER -m ruff check "$MODULE" --config "$PYPROJECT_TOML_PATH" > "${TMP_DIR}/${LOG_ALIAS}_ruff.log"
ruff_exit_status=$?

# mypy
$PYTHON_INTERPRETER -m mypy --config-file "$PYPROJECT_TOML_PATH" "$MODULE" >> "${TMP_DIR}/${LOG_ALIAS}_mypy.log"
mypy_exit_status=$?

set -e

# Display Results
cat "${TMP_DIR}/${LOG_ALIAS}_ruff.log"
cat "${TMP_DIR}/${LOG_ALIAS}_mypy.log"

# Return Exit Code
if [ $ruff_exit_status -eq 0 ] && [ $mypy_exit_status -eq 0 ]; then
  exit 0
else
  exit 1
fi
