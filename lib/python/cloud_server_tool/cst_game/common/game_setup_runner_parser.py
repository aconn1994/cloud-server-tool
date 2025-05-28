import argparse
import importlib

from cst_game.common.game_setup_runner_args import GameSetupRunnerArgs


def parse_and_run(
    supplied_args: list[str] = None, strict_mode: bool = False
) -> GameSetupRunnerArgs:
    parser = argparse.ArgumentParser(description="Game Setup Arg Parser")
    parser.add_argument(
        "--module-name",
        type=str,
        default=None,
        required=True,
        help="Module-style path to cst_game setup file: 'cst_game.games.arma_three.setup'",
    )

    parser.add_argument(
        "--operating-system",
        type=str,
        default=None,
        required=True,
        help="Operating system of system",
    )

    parser.add_argument(
        "--username",
        type=str,
        default=None,
        help="Username",
    )

    parser.add_argument(
        "--password",
        type=str,
        default=None,
        help="Password",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        required=False,
        help="Enable debug mode",
    )

    parser.add_argument(
        "--local",
        action="store_true",
        required=False,
        help="Run local mode",
    )

    namespace = GameSetupRunnerArgs()
    if strict_mode:
        parsed_args = parser.parse_args(args=supplied_args, namespace=namespace)
    else:
        parsed_args, unknown_args = parser.parse_known_args(
            args=supplied_args, namespace=namespace
        )
        if unknown_args:
            print(
                f"Strict Mode is False, ignoring extra supplied arguments: {unknown_args}"
            )

    print(f"Parsed args: {parsed_args}")

    module = importlib.import_module(parsed_args.module_name)
    _ = module.main(parsed_args=parsed_args)
    return parsed_args
