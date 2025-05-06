from cst_game.platform_config.abstract_platform_config import AbstractPlatformConfig


class DummyPlatformConfig(AbstractPlatformConfig):

    @property
    def binary_32bit(self) -> str:
        return "dummy_binary_32bit"

    @property
    def binary_64bit(self) -> str:
        return "dummy_binary_64bit"

    @property
    def username(self) -> str | None:
        return "dummy_username"

    @property
    def password(self) -> str | None:
        return "dummy_password"

def test_abstract_platform_config() -> None:
    dummy_platform_config = DummyPlatformConfig()

    assert dummy_platform_config.binary_32bit == "dummy_binary_32bit"
    assert dummy_platform_config.binary_64bit == "dummy_binary_64bit"
    assert dummy_platform_config.username == "dummy_username"
    assert dummy_platform_config.password == "dummy_password"