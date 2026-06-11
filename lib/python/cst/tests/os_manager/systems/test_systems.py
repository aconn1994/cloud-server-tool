import getpass
import os
import platform

from cst_game.os_manager.operating_system_manager import OperatingSystemManager


def test_linux_os() -> None:
    linux_os = OperatingSystemManager().name_to_os_mapper["linux"]

    assert linux_os.operating_system_alias == "linux"
    assert linux_os.instance_root_dir == f"/home/{linux_os.default_game_folder}"
    assert linux_os.operating_system_name == os.name
    assert linux_os.platform_system == platform.system()
    assert linux_os.system_version == platform.release()
    assert linux_os.user == getpass.getuser()


def test_macos_os() -> None:
    mac_os = OperatingSystemManager().name_to_os_mapper["macos"]

    assert mac_os.operating_system_alias == "macos"
    assert mac_os.instance_root_dir == f"/Users/{mac_os.default_game_folder}"
    assert mac_os.operating_system_name == os.name
    assert mac_os.platform_system == platform.system()
    assert mac_os.system_version == platform.release()
    assert mac_os.user == getpass.getuser()


def test_windows_os() -> None:
    windows_os = OperatingSystemManager().name_to_os_mapper["windows"]

    assert windows_os.operating_system_alias == "windows"
    assert windows_os.instance_root_dir == f"C:/Users/{windows_os.default_game_folder}"
    assert windows_os.operating_system_name == os.name
    assert windows_os.platform_system == platform.system()
    assert windows_os.system_version == platform.release()
    assert windows_os.user == getpass.getuser()
