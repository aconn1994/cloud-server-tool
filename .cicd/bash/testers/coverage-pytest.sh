#!/bin/bash

set -eo pipefail

PYTHONPATH=$1
MODULE=$2
LOG_ALIAS=$3
PYPROJECT_TOML_PATH=$4
PYTHON_INTERPRETER=$5

export PYTHONPATH
echo "PYTHONPATH is set to ${PYTHONPATH}"
echo "Running python tests with coverage in ${MODULE}"
cd "$MODULE"

# Run tests while delaying failures until end run
set +e
$PYTHON_INTERPRETER -m coverage run --rcfile="$PYPROJECT_TOML_PATH" -m pytest -c "$PYPROJECT_TOML_PATH" -ra -q -v -m "not excluded" > "$TMP_DIR/${LOG_ALIAS}_pytest.log"
coverage_run_exit_status=$?
$PYTHON_INTERPRETER -m coverage report --rcfile="$PYPROJECT_TOML_PATH" > "$TMP_DIR/${LOG_ALIAS}_coverage.log"
coverage_report_exit_status=$?
$PYTHON_INTERPRETER -m coverage html -d "$TMP_DIR/${LOG_ALIAS}_coverage"
#mv htmlcov "$TMP_DIR/${LOG_ALIAS}_coverage"
set -e

# Display Results
cat "$TMP_DIR/${LOG_ALIAS}_pytest.log"
cat "$TMP_DIR/${LOG_ALIAS}_coverage.log"

# Return Exit Code
if [ $coverage_run_exit_status -eq 0 ] && [ $coverage_report_exit_status -eq 0 ]; then
  exit 0
else
  exit 1
fi
