from cst_game.os_manager.abstract_os import AbstractOS


class MacOS(AbstractOS):
    operating_system_alias = "macos"

    def __init__(self) -> None:
        super().__init__()

    @property
    def instance_root_dir(self) -> str:
        return f"/Users/{self.user}"
