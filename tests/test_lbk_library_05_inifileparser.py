# command --> pytest --cov-report term-missing --cov=lbk_library ../tests/

# Test the IniFileParser functions

import os
from pathlib import Path
import platform
import sys

import pytest

if "/home/larry/development/lbk_library/src" not in sys.path:
    sys.path.append("/home/larry/development/lbk_library/src")

from lbk_library import IniFileParser

#if not os.environ["HOME"]:
os.environ["HOME"] = str(Path.home())
print('os.environ["HOME"]', os.environ["HOME"])


sample_config = {
    "section_1": {
        "data_1": "10",
        "data_2": "this is a string",
    },
    "section_2": {"data_3": "10.5", "data_4": "name", "data_5": "True"},
    "section_3": {},
}

sample_ini = [
    "[section_1]",
    "data_1 = 10",
    "data_2 = this is a string",
    "",
    "[section_2]",
    "data_3 = 10.5",
    "data_4 = name",
    "",
    "[section_3]",
]


def test_01_bare_constructor():
    """Test constructor with file name only, default for config_sub_dir"""
    filename = "testfile.ini"
    default_dir = "testfile"
    default_config_dir = os.path.join(os.environ["HOME"], ".config", default_dir)
    default_config_file = os.path.join(default_config_dir, filename)
    parser = IniFileParser(filename)
    assert parser.config_file == default_config_file
    os.rmdir(default_config_dir)
# end test_01_bare_constructor()

def test_02_constructor():
    """Test constructor with file name and config_sub_dir"""
    filename = "testfile.ini"
    config_sub_dir = "testfile"
    default_config_dir = os.path.join(os.environ["HOME"], ".config", config_sub_dir)
    default_config_file = os.path.join(default_config_dir, filename)
    parser = IniFileParser(filename, config_sub_dir)
    assert parser.config_file == default_config_file
    os.rmdir(default_config_dir)
# end test_02_constructor()

def test_03_constructor():
    """
    Test constructor with file name, config_sub_dir and non-standard
    destination dir
    """
    filename = "testfile.ini"
    config_sub_dir = "testfile"
    current_dir = os.getcwd()
    test_config_dir = os.path.join(current_dir, config_sub_dir)
    test_config_file = os.path.join(test_config_dir, filename)
    parser = IniFileParser(filename, config_sub_dir, current_dir)
    assert parser.config_file == test_config_file
    os.rmdir(test_config_dir)
# end test_03_constructor()

def test_04_read_empty_config():
    # File name, subdirectory, and config_dir
    filename = "testfile.ini"
    subdir = "myTesting"
    config_dir = os.path.join(os.environ["HOME"], ".config", subdir)
    # reads empty file
    parser = IniFileParser(filename, subdir)
    config = parser.read_config()
    assert isinstance(config, dict)
    assert len(config) == 0
    os.rmdir(config_dir)
# end test_04_read_empty_config()

def test_05_write_empty_config():
    filename = "testfile.ini"
    subdir = "myTesting"
    config_dir = os.path.join(os.environ["HOME"], ".config", subdir)
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
    # cleanup
    os.remove(parser.config_file)
    os.rmdir(config_dir)
# end test_05_write_empty_config()

def test_06_write_config():
    # Write sample config file from a dict to local directory
    filename = "testfile.ini"
    subdir = "myTesting"
    config_dir = os.path.join(os.environ["HOME"], ".config", subdir)
    # write and check sample file
    parser = IniFileParser(filename, subdir)
    parser.write_config(sample_config)
    assert os.path.exists(parser.config_file)
    # get sample file and verify same as sample_config
    config = parser.read_config()
    assert isinstance(config, dict)
    assert len(config) == len(sample_config)
    assert config == sample_config
    os.remove(parser.config_file)
    os.rmdir(config_dir)
# end test_06_write_config()

# end lbk_library_05_inifileparser.py
