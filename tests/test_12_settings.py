"""
Test the Settings class.

File:       test_12_settings.py
Author:     Lorn B Kerr
Copyright:  (c) 2025 Lorn B Kerr
License:    MIT, see file LICENSE
"""

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from PySide6.QtCore import QSettings

from lbk_library.gui import Settings
from lbk_library.testing_support.core_setup import filesystem

line_1_value = "line 1 text."


def setup(tmp_path):
    base_directory = filesystem(tmp_path)
    config_dir = base_directory + "/" + ".config"
    settings = Settings("Test Config", "test_config")
    settings.setValue("line1", line_1_value)
    settings.sync()
    return (settings, config_dir)


def test_12_01_class_type(tmp_path):
    settings, config_dir = setup(tmp_path)

    assert isinstance(settings, Settings)
    assert isinstance(settings, QSettings)
    assert settings.value("line1") == line_1_value


def test_12_02_write_read_array(tmp_path):
    settings, config_dir = setup(tmp_path)
    old_array = ["a", "b", "asd"]

    settings.write_list("test", old_array)
    new_array = settings.read_list("test")
    assert len(new_array) == len(old_array)
    for i in range(len(old_array)):
        assert new_array[i] == old_array[i]



def test_12_03_boolean_value(tmp_path):
    settings, config_dir = setup(tmp_path)
    value = 0
    result = settings.set_bool_value("test", value)
    assert not result
    assert not settings.bool_value("test")

    for value in (True, "1", 1, True, "True", "true"):
        assert settings.set_bool_value("test", value)
        assert settings.bool_value("test")

    for value in (None, "False", "me"):
        assert not settings.bool_value("new_test")

       
