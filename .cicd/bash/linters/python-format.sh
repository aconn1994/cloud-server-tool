#!/bin/bash

set -eo pipefail

PYTHONPATH=$1
MODULE=$2
LOG_ALIAS=$3
CHECK_ARG=$4
PYPROJECT_TOML_PATH=$5
PYTHON_INTERPRETER=$6

export PYTHONPATH
echo "PYTHONPATH is set to ${PYTHONPATH}"
echo "Format ${CHECK_ARG}: ${MODULE}"

set +e

if [ "$CHECK_ARG" ]; then
  $PYTHON_INTERPRETER -m ruff check "$MODULE" --config "$PYPROJECT_TOML_PATH" > "${TMP_DIR}/${LOG_ALIAS}_ruff_check.log"
  init_scanner_exit_status=$?

  $PYTHON_INTERPRETER -m ruff format "$MODULE" --config "$PYPROJECT_TOML_PATH" >> "${TMP_DIR}/${LOG_ALIAS}_ruff_format.log"
  ruff_exit_status=$?

  $PYTHON_INTERPRETER -m mypy --config-file "$PYPROJECT_TOML_PATH" "$MODULE" >> "${TMP_DIR}/${LOG_ALIAS}_mypy.log"
  mypy_exit_status=$?

else
  $PYTHON_INTERPRETER -m ruff check --fix "$MODULE" --config "$PYPROJECT_TOML_PATH" > "${TMP_DIR}/${LOG_ALIAS}_ruff_check_fix.log"
  init_scanner_exit_status=$?

  $PYTHON_INTERPRETER -m ruff format "$MODULE" --config "$PYPROJECT_TOML_PATH" >> "${TMP_DIR}/${LOG_ALIAS}_ruff_format_check.log"
  ruff_exit_status=$?

  $PYTHON_INTERPRETER -m mypy --config-file "$PYPROJECT_TOML_PATH" "$MODULE" >> "${TMP_DIR}/${LOG_ALIAS}_mypy.log"
  mypy_exit_status=$?

fi

set -e

# Display Results
cat "$TMP_DIR"/"${LOG_ALIAS}"*


# Return Exit Code
if [ $init_scanner_exit_status -eq 0 ] && [ $ruff_exit_status -eq 0 ] && [ $mypy_exit_status -eq 0 ]; then
  exit 0
else
  exit 1
fi
