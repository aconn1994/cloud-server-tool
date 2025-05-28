from argparse import Namespace


class GameSetupRunnerArgs(Namespace):
    module_name: str
    operating_system: str
    debug: bool
