import os
import shutil

from cst_game.common.utils import Utils

utils = Utils()
dummy_dir_name = "DUMMY_DIR"
dummy_file_name = "DUMMY_FILE.txt"
dummy_sub_dir_name = "DUMMY_SUBDIR"
dummy_sub_file_name = "DUMMY_SUBFILE.txt"


def test_reformat_string():
    string_to_reformat = "this-is-a-test"
    reformatted_string = "this_is_a_test"
    assert utils.reformat_string(string_to_reformat, "_") == reformatted_string


def test_rename_file():
    dummy_file_1_name = "dummy_file_1.txt"
    dummy_file_2_name = "dummy_file_2.txt"

    open(dummy_file_1_name, "w")
    utils.rename(
        item_path="", item_name=dummy_file_1_name, new_item_name=dummy_file_2_name
    )
    assert os.path.exists(dummy_file_2_name)
    os.remove(dummy_file_2_name)


def test_symlink():
    dummy_tmp_src_dir = "tmp_src"
    dummy_tmp_dst_dir = "tmp_dst"

    os.mkdir(dummy_tmp_src_dir)
    open(os.path.join(dummy_tmp_src_dir, dummy_file_name), "w")

    utils.symlink(dummy_tmp_src_dir, dummy_tmp_dst_dir, "Dummy Directory")
    assert os.path.islink(os.path.join(dummy_tmp_dst_dir))
    utils.symlink(dummy_tmp_src_dir, dummy_tmp_dst_dir, "Dummy Directory")
    shutil.rmtree(dummy_tmp_src_dir)
    os.unlink(dummy_tmp_dst_dir)


def test_recursive_rename_directory_lower():
    os.mkdir(os.path.join(os.getcwd(), dummy_dir_name))
    open(os.path.join(dummy_dir_name, dummy_file_name), "w")
    os.mkdir(os.path.join(os.getcwd(), dummy_dir_name, dummy_sub_dir_name))
    open(os.path.join(dummy_dir_name, dummy_sub_dir_name, dummy_sub_file_name), "w")

    utils.recursive_rename_directory(os.getcwd(), case="lower")

    assert os.path.exists(os.path.join(dummy_dir_name.lower()))
    assert os.path.exists(os.path.join(dummy_dir_name.lower(), dummy_file_name.lower()))
    assert os.path.exists(
        os.path.join(dummy_dir_name.lower(), dummy_sub_dir_name.lower())
    )
    assert os.path.exists(
        os.path.join(
            dummy_dir_name.lower(),
            dummy_sub_dir_name.lower(),
            dummy_sub_file_name.lower(),
        )
    )

    shutil.rmtree(os.path.join(os.getcwd(), dummy_dir_name.lower()))


def test_recursive_rename_directory_upper():
    os.mkdir(os.path.join(os.getcwd(), dummy_dir_name))
    open(os.path.join(dummy_dir_name, dummy_file_name), "w")
    os.mkdir(os.path.join(os.getcwd(), dummy_dir_name, dummy_sub_dir_name))
    open(os.path.join(dummy_dir_name, dummy_sub_dir_name, dummy_sub_file_name), "w")

    utils.recursive_rename_directory(os.getcwd(), case="upper")

    assert os.path.exists(os.path.join(dummy_dir_name.upper()))
    assert os.path.exists(os.path.join(dummy_dir_name.upper(), dummy_file_name.upper()))
    assert os.path.exists(
        os.path.join(dummy_dir_name.upper(), dummy_sub_dir_name.upper())
    )
    assert os.path.exists(
        os.path.join(
            dummy_dir_name.upper(),
            dummy_sub_dir_name.upper(),
            dummy_sub_file_name.upper(),
        )
    )

    shutil.rmtree(os.path.join(os.getcwd(), dummy_dir_name.upper()))
