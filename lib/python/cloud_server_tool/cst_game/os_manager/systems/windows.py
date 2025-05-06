from cst_game.os_manager.abstract_os import AbstractOS


class Windows(AbstractOS):
    operating_system_alias = "windows"
    def __init__(self) -> None:
        super().__init__()

    @property
    def instance_root_dir(self) -> str:
        return f"C:/Users/{self.user}"
