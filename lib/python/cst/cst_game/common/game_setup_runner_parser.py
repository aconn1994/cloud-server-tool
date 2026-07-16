import argparse
import importlib

from cst_game.common.game_setup_runner_args import GameSetupRunnerArgs


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None) -> None:  # type: ignore
        setattr(namespace, self.dest, dict())
        for value in values:
            if "=" not in value:
                raise argparse.ArgumentError(self, f"Invalid format: '{value}'. Must be key=value.")
            key, val = value.split("=", 1)
            getattr(namespace, self.dest)[key] = val


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

    parser.add_argument(
        "--arch",
        type=str,
        default="64",
        help="Preferred architecture executable",
    )

    parser.add_argument(
        "--expedite-launch",
        action="store_true",
        required=False,
        help="Skip installs and updates. Used for skipping SteamCMD limits.",
    )

    parser.add_argument("--kwargs", nargs="*", action=ParseKwargs, help="Pass pairs like key=value")

    namespace = GameSetupRunnerArgs()
    if strict_mode:
        parsed_args = parser.parse_args(args=supplied_args, namespace=namespace)
    else:
        parsed_args, unknown_args = parser.parse_known_args(args=supplied_args, namespace=namespace)
        if unknown_args:
            print(f"Strict Mode is False, ignoring extra supplied arguments: {unknown_args}")

    print(f"Parsed args: {parsed_args}")

    module = importlib.import_module(parsed_args.module_name)
    _ = module.main(parsed_args=parsed_args)
    return parsed_args
