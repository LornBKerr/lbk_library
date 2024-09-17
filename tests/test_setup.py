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
 License:    MIT, see file License
 """

import os
import sys
from typing import Any

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from PyQt5 import QtCore, QtGui, QtWidgets

from lbk_library import DataFile, Element, ElementSet
from lbk_library.gui import ComboBox, ErrorFrame, LineEdit

datafile_name = "test_file.data"

datafile_definition = [
    (
        'CREATE TABLE IF NOT EXISTS "elements"'
        '("record_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,'
        ' "installed" BOOLEAN,'
        ' "remarks" TEXT DEFAULT NULL)'
    ),
]

# tool_tips = [
#    "Tool Tip 0",
#    "Tool Tip 1",
#    "Tool Tip 2",
# ]
# cell_alignments = [
#    Qt.AlignmentFlag.AlignLeft,
#    Qt.AlignmentFlag.AlignHCenter,
#    Qt.AlignmentFlag.AlignRight,
# ]
#
column_names = ["record_id", "name", "species", "tank_number", "remarks"]

fish_value_set = [
    [1, "Sammy", "shark", 1, "remark 1"],
    [2, "Jamie", "cuttlefish", 7, "remark 2"],
]
#
# test_record = {
#    "record_id": 1,
#    "name": "Sammy",
#    "species": "shark",
#    "tank_number": 1,
#    "remarks": "remark 1",
# }

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
element_record = {
    "record_id": 1,
    "remarks": "remark 1",
}

element_values = {
    "record_id": 9876,
    "remarks": "test",
}


def new_element(datafile, properties={}):
    # create a new Element from properties
    element = Element(datafile, "elements")
    element.set_initial_values(properties)
    element.set_properties(properties)
    element.clear_value_changed_flags()
    return element


def better_element(datafile, properties={}):
    # create a new Element from properties
    better_element = Element(datafile, "elements")
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
        self.close_button = QtWidgets.QPushButton(test_form)
        self.close_button.setObjectName("close_button")
        self.close_button.setToolTip("Close the form, any unsaved changes will be lost")
        self.close_button.setText("Cancel / Close")

        self.change_button = QtWidgets.QPushButton(test_form)
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


class Fish(Element):
    def __init__(self, datafile: DataFile, table_name: str, record_id: int = 0) -> None:
        super().__init__(datafile, table_name)
        properties = self.get_properties_from_datafile("record_id", record_id)
        self.set_properties(properties)
        self.set_initial_values(self.get_properties())
        self.clear_value_changed_flags()

    def set_properties(self, properties: dict[str, Any]) -> None:
        if properties is not None and isinstance(properties, dict):
            # Handle the 'record_id' and 'remarks' entries
            results = super().set_properties(properties)
            # Handle all the other properties here
            for key in properties.keys():
                if key == "name":
                    results[key] = self.set_name(properties[key])
                if key == "species":
                    results[key] = self.set_species(properties[key])
                if key == "tank_number":
                    results[key] = self.set_tank_number(properties[key])
        return results

    def get_name(self) -> str:
        name = self._get_property("name")
        if name is None:
            name = ""
        return name

    def set_name(self, name: str) -> dict[str, Any]:
        result = self.validate.text_field(name, self.validate.REQUIRED, 1, 10)
        if result["valid"]:
            self._set_property("name", result["entry"])
        else:
            self._set_property("name", "")
        return result

    def get_species(self) -> str:
        type = self._get_property("species")
        if species is None:
            species = ""
        return type

    def set_species(self, species: str) -> dict[str, Any]:
        result = self.validate.text_field(species, self.validate.REQUIRED, 1, 10)
        if result["valid"]:
            self._set_property("species", result["entry"])
        else:
            self._set_property("species", "")
        return result

    def get_tank_number(self) -> str:
        type = self._get_property("tank_number")
        if tank_number is None:
            tank_number = 0
        return type

    def set_tank_number(self, tank_number: int) -> dict[str, Any]:
        result = self.validate.integer_field(tank_number, self.validate.REQUIRED, 1, 10)
        if result["valid"]:
            self._set_property("tank_number", result["entry"])
        else:
            self._set_property("tank_number", 0)
        return result


class FishSet(ElementSet):
    def __init__(
        self,
        datafile,
        table_name,
        where_column: str = None,
        where_value: str | int = None,
        order_by_column: str = None,
    ):
        table_name = "fish"
        element_type = Fish
        super().__init__(
            datafile,
            table_name,
            element_type,
            where_column,
            where_value,
            order_by_column,
        )
