import os
import re
from typing import Literal


class Utils:
    @staticmethod
    def reformat_string(
        val: str, repl_char: str, pattern: str = "[^A-Za-z0-9]+"
    ) -> str:
        return re.sub(pattern, repl_char, val)

    @staticmethod
    def rename(item_path: str, item_name: str, new_item_name: str) -> None:
        os.rename(
            os.path.join(item_path, item_name), os.path.join(item_path, new_item_name)
        )

    @staticmethod
    def symlink(src: str, dst: str, descriptor: str) -> None:
        try:
            os.symlink(src, dst)
        except FileExistsError:
            print(f"{descriptor} already linked to {dst}.")

    def recursive_rename_directory(
        self, directory: str, case: Literal["lower", "upper"]
    ) -> None:
        for item in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, item)):
                self.recursive_rename_directory(os.path.join(directory, item), case)
                if case == "lower":
                    self.rename(directory, item, item.lower())
                elif case == "upper":
                    self.rename(directory, item, item.upper())
            else:
                if case == "lower":
                    self.rename(directory, item, item.lower())
                elif case == "upper":
                    self.rename(directory, item, item.upper())
