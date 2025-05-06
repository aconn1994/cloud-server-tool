from cst_game.os_manager.abstract_os import AbstractOS
from cst_game.os_manager.systems.linux import Linux
from cst_game.os_manager.systems.macos import MacOS
from cst_game.os_manager.systems.windows import Windows


class OperatingSystemManager:
    @property
    def name_to_os_mapper(self) -> dict[str, AbstractOS]:
        return {  # type: ignore
            Linux.operating_system_alias: Linux(),  # type: ignore
            MacOS.operating_system_alias: MacOS(),  # type: ignore
            Windows.operating_system_alias: Windows(),  # type: ignore
        }
