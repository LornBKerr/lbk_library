# command --> pytest --cov-report term-missing --cov=lbk_library ../tests/

# Test the IniFileParser functions

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import IniFileParser

# define the standard directory locations that are os specific for Linux and Windows
HOME = os.path.expanduser("~")
BASE_DIR = os.path.abspath(".")
SRC_DIR = os.path.join(BASE_DIR, "src")
CONFIG_DIR = ""

if sys.platform.startswith("linux"):
    if "XDG_CONFIG_HOME" in os.environ:
        CONFIG_DIR = os.environ["XDG_CONFIG_HOME"]
    else:
        CONFIG_DIR = os.path.join(HOME, ".config")

elif sys.platform.startswith("win"):
    # force config dir to be in {APPDATA}\Local
    CONFIG_DIR = os.path.join(HOME, "AppData", "Local")


sample_config = {
    "section_1": {
        "data_1": "10",
        "data_2": "this is a string",
    },
    "section_2": {"data_3": "10.5", "data_4": "name", "data_5": "True"},
    "section_3": {},
}


def test_01_bare_constructor_get_config_dir_path():
    # Verify the config path exists
    filename = "testfile.ini"
    sub_dir = os.path.splitext(filename)[0]
    test_path = os.path.join(CONFIG_DIR, sub_dir, filename)
    parser = IniFileParser(filename)
    parser_path = parser.config_path()
    assert test_path == parser_path
    # end test_01_get_config_dir_path()


def test_02_constructor(tmpdir):
    """Test constructor with file name and config_sub_dir"""
    filename = "testfile.ini"
    config_sub_dir = tmpdir.join("testfile")
    expected_path = tmpdir.join("testfile", filename)
    parser = IniFileParser(filename, config_sub_dir)
    parser_path = parser.config_path()
    assert expected_path == parser_path
    # end test_02_constructor()


def test_03_constructor(tmpdir):
    """
    Test constructor with file name, config_sub_dir and config dir
    """
    filename = "testfile.ini"
    config_sub_dir = tmpdir.join("testfile")
    config_dir = "test"
    expected_path = tmpdir.join("testfile", "test", filename)
    parser = IniFileParser(filename, config_dir, config_sub_dir)
    parser_path = parser.config_path()
    assert parser_path == expected_path
    # end test_03_constructor()


def test_04_read_empty_config(tmpdir):
    filename = "testfile.ini"
    subdir = tmpdir.join("testfile")
    parser = IniFileParser(filename, subdir)
    config = parser.read_config()
    assert isinstance(config, dict)
    assert len(config) == 0
    # end test_04_read_empty_config()


def test_05_write_empty_config(tmpdir):
    filename = "testfile.ini"
    subdir = tmpdir.join("testfile")
    # write and check empty file
    ini_file = {}
    parser = IniFileParser(filename, subdir)
    parser.write_config(ini_file)
    assert os.path.exists(parser.config_file)
    assert os.path.getsize(parser.config_file) == 0
    # read and check the empty file
    parser = IniFileParser(filename, subdir)
    config = parser.read_config()
    assert isinstance(config, dict)
    assert len(config) == 0
    # end test_05_write_empty_config()


def test_06_write_config(tmpdir):
    filename = "testfile.ini"
    subdir = tmpdir.join("testfile")
    # write and check sample file
    parser = IniFileParser(filename, subdir)
    parser.write_config(sample_config)
    assert os.path.exists(parser.config_file)
    # get sample file and verify same as sample_config
    config = parser.read_config()
    assert isinstance(config, dict)
    assert len(config) == len(sample_config)
    assert config == sample_config
    # end test_06_write_config()


# end testlbk_library_05_inifileparser.py
