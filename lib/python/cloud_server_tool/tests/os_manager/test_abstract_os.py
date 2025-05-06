import getpass
import os
import platform

from cst_game.os_manager.abstract_os import AbstractOS


class DummyAbstractOS(AbstractOS):
    @property
    def operating_system_alias(self) -> str:
        return "dummy_os_alias"

    @property
    def instance_root_dir(self) -> str:
        return "/os/rootdir"


def test_dummy_abstract_os() -> None:
    dummy_abstract_os = DummyAbstractOS()
    assert dummy_abstract_os.operating_system_alias == "dummy_os_alias"
    assert dummy_abstract_os.instance_root_dir == "/os/rootdir"
    assert dummy_abstract_os.operating_system_name == os.name
    assert dummy_abstract_os.platform_system == platform.system()
    assert dummy_abstract_os.system_version == platform.release()
    assert dummy_abstract_os.user == getpass.getuser()
