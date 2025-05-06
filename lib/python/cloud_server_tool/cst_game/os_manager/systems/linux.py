from cst_game.os_manager.abstract_os import AbstractOS


class Linux(AbstractOS):
    operating_system_alias = "linux"
    def __init__(self) -> None:
        super().__init__()

    @property
    def instance_root_dir(self) -> str:
        return f"/home/{self.user}"
