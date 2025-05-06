import pytest
from cst_game.common.game_setup_runner_args import GameSetupRunnerArgs
from cst_game.common.game_setup_runner_parser import parse_and_run

MODULE_NAME = "tests.common.module_for_test_game_setup_runner_parser"
NON_EXIST_MODULE_NAME = "tests.common.nonexistent_module_name"
OPERATING_SYSTEM = "linux"
NON_EXIST_OPERATING_SYSTEM = "chromeOS"
UNKNOWN_ARG = "unknown"
base_args = ["--module-name", MODULE_NAME, "--operating-system", OPERATING_SYSTEM]
base_args_w_equals = [
    f"{base_args[0]}={base_args[1]}",
    f"{base_args[2]}={base_args[3]}",
]
base_args_w_unknown_args = [
    "--module-name",
    MODULE_NAME,
    "--operating-system",
    OPERATING_SYSTEM,
    "--unknown-arg",
    UNKNOWN_ARG,
]
base_args_w_non_exist_module_name = [
    "--module-name",
    NON_EXIST_MODULE_NAME,
    "--operating-system",
    NON_EXIST_OPERATING_SYSTEM,
]


def test_parse_and_run_crashes_missing_module_name():
    with pytest.raises(SystemExit):
        parse_and_run(supplied_args=[])


def test_parse_and_run_crashes_nonexistent_module_name():
    with pytest.raises(ModuleNotFoundError):
        parse_and_run(supplied_args=base_args_w_non_exist_module_name)


def test_parse_and_run_works_with_base_args():
    result = parse_and_run(supplied_args=base_args)
    assert isinstance(result, GameSetupRunnerArgs)
    assert result.module_name == MODULE_NAME
    assert result.operating_system == OPERATING_SYSTEM


def test_parse_and_run_works_with_base_args_with_equals():
    result = parse_and_run(supplied_args=base_args_w_equals)
    assert isinstance(result, GameSetupRunnerArgs)
    assert result.module_name == MODULE_NAME
    assert result.operating_system == OPERATING_SYSTEM


def test_parse_and_run_works_with_base_args_with_unknown_args():
    result = parse_and_run(supplied_args=base_args_w_unknown_args)
    assert isinstance(result, GameSetupRunnerArgs)
    assert result.module_name == MODULE_NAME
    assert result.operating_system == OPERATING_SYSTEM


def test_parse_and_run_works_with_base_args_with_strict_mode():
    result = parse_and_run(supplied_args=base_args, strict_mode=True)
    assert isinstance(result, GameSetupRunnerArgs)
    assert result.module_name == MODULE_NAME
    assert result.operating_system == OPERATING_SYSTEM
