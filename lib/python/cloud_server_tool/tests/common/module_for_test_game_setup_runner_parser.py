from cst_game.common.game_setup_runner_args import GameSetupRunnerArgs


def main(parsed_args: GameSetupRunnerArgs) -> str:
    print(parsed_args)
    return "Success"
