from argparse import Namespace


class GameSetupRunnerArgs(Namespace):
    module_name: str
    operating_system: str
    username: str | None
    password: str | None
    debug: bool
    local: bool
    arch: str
    expedite_launch: bool
