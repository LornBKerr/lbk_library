"""
Test the Settings class.

File:       test_12_settings.py
Author:     Lorn B Kerr
Copyright:  (c) 2025 Lorn B Kerr
License:    MIT, see file LICENSE
"""

import os
import sys

# from copy import deepcopy

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from PySide6.QtCore import QSettings

from lbk_library.gui import Settings
from lbk_library.testing_support.core_setup import (  # datafile_close,; datafile_create,; load_datafile_table,
    filesystem,
)

# from PySide6.QtGui import QBrush, QColor


line_1_value = "line 1 text."


def setup_table_model(tmp_path):
    base_directory = filesystem(tmp_path)
    config_dir = base_directory + "/" + ".config"
    settings = Settings("Test Config", "test_config")
    settings.setValue("line1", line_1_value)
    settings.sync()
    return (settings, config_dir)


def test_12_01_class_type(tmp_path):
    settings, config_dir = setup_table_model(tmp_path)

    assert isinstance(settings, Settings)
    assert isinstance(settings, QSettings)
    assert settings.value("line1") == line_1_value


def test_12_02_write_read_array(tmp_path):
    settings, config_dir = setup_table_model(tmp_path)

    old_array = ["a", "b", "asd"]

    # write the array
    settings.beginGroup("array")
    settings.write_list(old_array, "test")
    settings.endGroup()

    settings.beginGroup("array")
    new_array = settings.read_list("test")
    settings.endGroup()

    assert len(new_array) == len(old_array)
    for i in range(len(old_array)):
        assert new_array[i] == old_array[i]
