"""
Test setup for the lbk_library functionality.

Values Available:
    test_string - A string for testing where a string is needed.
    long_string - A string exceeding the base 255 character upper limit.

Filesystem, Directories and associated files:
    directories (list): List of directories for the filesystem.
    filesystem(tmp_path): Pytest fixture to generate a temporary
        filesystem.

File:       test_setup.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file LICENSE
"""

import os
import sys
from typing import Any

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from PySide6.QtWidgets import QPushButton

from lbk_library import Element  # DataFile, , ElementSet
from lbk_library.gui import ComboBox, ErrorFrame, LineEdit

datafile_name = "test_file.data"
datafile_table = "elements"

datafile_definition = [
    (
        'CREATE TABLE IF NOT EXISTS "elements"'
        '("record_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,'
        ' "installed" BOOLEAN,'
        ' "remarks" TEXT DEFAULT NULL)'
    ),
]

# set element values from array of values
element_values = {
    "record_id": 9876,
    "remarks": "test",
}

# set element values from dict of values
element_definition = [
    (
        'CREATE TABLE IF NOT EXISTS "elements" '
        '("record_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,'
        ' "remarks" TEXT DEFAULT NULL)'
    ),
]


def new_element(datafile, properties={}):
    # create a new Element from properties
    element = Element(datafile, datafile_table)
    element.set_initial_values(properties)
    element.set_properties(properties)
    element.clear_value_changed_flags()
    return element


def better_element(datafile, properties={}):
    # create a new Element from properties
    better_element = Element(datafile, datafile_table)
    better_element.set_initial_values(properties)
    better_element.set_properties(properties)
    better_element.clear_value_changed_flags()
    return better_element


# define a do nothing function to act as the 'save_action' parameter of
# the dialog,action_cancel() function.
def save_something(action):
    pass


class DummyForm:
    def __init__(self, test_form):
        self.close_button = QPushButton(test_form)
        self.close_button.setObjectName("close_button")
        self.close_button.setToolTip("Close the form, any unsaved changes will be lost")
        self.close_button.setText("Cancel / Close")

        self.change_button = QPushButton(test_form)
        self.change_button.setObjectName("change_button")
        self.change_button.setToolTip(
            "Save the updated assembly changes, then clear the form"
        )
        self.change_button.setText("Change")

        self.combo_error_frame = ErrorFrame(test_form)
        self.combo_error_frame.setObjectName("combo_error_frame")
        self.combo_box = ComboBox(self.combo_error_frame)
        self.combo_box.setObjectName("combo_box")

        self.edit_error_frame = ErrorFrame(test_form)
        self.edit_error_frame.setObjectName("edit_error_frame")

        self.line_edit = LineEdit(self.edit_error_frame)
        self.line_edit.setObjectName("line_edit")
        self.line_edit.setToolTip("Required: Enter the info, 1 to 15 Characters")
