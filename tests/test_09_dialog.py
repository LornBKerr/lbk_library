"""
Test the Dialog class.

File:       test_09_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from PySide6.QtWidgets import QDialog, QMainWindow, QMessageBox
from test_setup import (
    DummyForm,
    better_element,
    datafile_definition,
    element_values,
    new_element,
    save_something,
)

from lbk_library import DataFile, Element
from lbk_library.gui import Dialog, ErrorFrame, LineEdit, combo_box
from lbk_library.testing_support import (
    datafile_close,
    datafile_create,
    directories,
    filesystem,
    long_string,
    test_string,
)


def base_setup(filesystem, qtbot):
    datafile_name = directories[2] + "/test_data.data"
    filename = filesystem + "/" + datafile_name
    datafile = datafile_create(filename, datafile_definition)
    main = QMainWindow()
    dialog = Dialog(main, datafile, Dialog.VIEW_ELEMENT)
    dialog.form = DummyForm(dialog)
    qtbot.addWidget(main)
    return (dialog, main, datafile)


def test_09_01_class_type(filesystem, qtbot):
    dialog, main, datafile = base_setup(filesystem, qtbot)
    assert isinstance(dialog, Dialog)
    assert isinstance(dialog, QDialog)

    #    assert dialog.error_count == 0
    datafile_close(datafile)


def test_09_02_get_datafile(filesystem, qtbot):
    dialog, main, datafile = base_setup(filesystem, qtbot)
    assert dialog.get_datafile() == datafile


def test_09_03_get_set_element(filesystem, qtbot):
    dialog, main, datafile = base_setup(filesystem, qtbot)
    assert dialog.get_element() is None
    dialog.set_element(new_element(datafile))
    qtbot.addWidget(main)
    assert isinstance(dialog.get_element(), Element)
    dialog.set_element(better_element(datafile))
    assert isinstance(dialog.get_element(), Element)
    datafile_close(datafile)


def test_09_04_msg_info_close(filesystem, qtbot):
    dialog, main, datafile = base_setup(filesystem, qtbot)
    msg = "Testing Information Box"
    msg_box = dialog.message_information_close(msg)
    assert msg_box.icon() == QMessageBox.Icon.Information
    assert msg_box.windowTitle() == "Success"
    assert msg_box.text() == msg
    assert (
        msg_box.standardButtons()
        == QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    datafile_close(datafile)


def test_09_05_msg_quest_changed_close(filesystem, qtbot):
    dialog, main, datafile = base_setup(filesystem, qtbot)
    changed_name = "description"
    msg = "Do you want to save the current changes before closing form?"
    msg_box = dialog.message_question_changed_close(changed_name)
    assert msg_box.icon() == QMessageBox.Icon.Question
    assert msg_box.windowTitle() == changed_name + " Changed"
    assert msg_box.text() == msg
    assert (
        msg_box.standardButtons()
        == QMessageBox.StandardButton.Yes
        | QMessageBox.StandardButton.No
        | QMessageBox.StandardButton.Cancel
    )
    datafile_close(datafile)


def test_09_06_msg_quest_change(filesystem, qtbot):
    dialog, main, datafile = base_setup(filesystem, qtbot)
    changed_name = "description"
    msg = "Do you want to save the current changes before reloading form?"
    msg_box = dialog.message_question_changed(changed_name)
    assert msg_box.icon() == QMessageBox.Icon.Question
    assert msg_box.windowTitle() == changed_name + " Changed"
    assert msg_box.text() == msg
    assert (
        msg_box.standardButtons()
        == QMessageBox.StandardButton.Yes
        | QMessageBox.StandardButton.No
        | QMessageBox.StandardButton.Cancel
    )


def test_09_07_msg_quest_no_changes(filesystem, qtbot):
    dialog, main, datafile = base_setup(filesystem, qtbot)
    title = "Form Entries Have Not Changed"
    msg = "Nothing has changed, so nothing to save"
    msg_box = dialog.message_question_no_changes()
    assert msg_box.icon() == QMessageBox.Icon.Question
    assert msg_box.windowTitle() == title
    assert msg_box.text() == msg
    assert msg_box.standardButtons() == QMessageBox.StandardButton.Ok
    datafile_close(datafile)


def test_09_08_msg_warning_selectio(filesystem, qtbot):
    dialog, main, datafile = base_setup(filesystem, qtbot)
    name = "Source"
    action = "Save"
    msg = "Nothing to "
    msg_box = dialog.message_warning_selection(name, action)
    assert msg_box.icon() == QMessageBox.Icon.Warning
    assert msg_box.windowTitle() == name + " not selected"
    assert msg_box.text() == msg + action
    assert msg_box.standardButtons() == QMessageBox.StandardButton.Ok
    datafile_close(datafile)


def test_09_09_msg_warning_failed(filesystem, qtbot):
    dialog, main, datafile = base_setup(filesystem, qtbot)
    operation = "Add"
    msg = "The " + operation + " operation failed for some reason."
    msg_box = dialog.message_warning_failed(operation)
    assert msg_box.icon() == QMessageBox.Icon.Warning
    assert msg_box.windowTitle() == operation + " Operation Failed"
    assert msg_box.text() == msg
    assert msg_box.standardButtons() == QMessageBox.StandardButton.Ok
    datafile_close(datafile)


def test_09_10_msg_warning_invalid(filesystem, qtbot):
    dialog, main, datafile = base_setup(filesystem, qtbot)
    error_msg = "3 Entries Missing"
    msg_box = dialog.message_warning_invalid()
    assert msg_box.icon() == QMessageBox.Icon.Warning
    assert msg_box.windowTitle() == "Form Entries Invalid"
    assert msg_box.text() == "Please correct the highlighted errors"
    assert msg_box.standardButtons() == QMessageBox.StandardButton.Ok
    msg_box = dialog.message_warning_invalid(error_msg)
    assert msg_box.icon() == QMessageBox.Icon.Warning
    assert msg_box.windowTitle() == "Form Entries Invalid"
    assert msg_box.text() == "Please correct the highlighted errors\n" + error_msg
    assert msg_box.standardButtons() == QMessageBox.StandardButton.Ok
    datafile_close(datafile)


def test_09_11_action_cancel(filesystem, qtbot, mocker):
    dialog, main, datafile = base_setup(filesystem, qtbot)
    dialog.form = DummyForm(dialog)
    dialog.set_element(new_element(datafile, element_values))
    # dialog is unchanged, just close
    assert dialog.action_cancel(save_something, 0)

    dialog = Dialog(main, datafile, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
    dialog.form = DummyForm(dialog)
    dialog.set_element(new_element(datafile, element_values))
    dialog.get_element().set_record_id(3456)
    # dialog is changed,
    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.No
    assert dialog.action_cancel(save_something, 0)

    dialog = Dialog(main, datafile, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)

    dialog.form = DummyForm(dialog)
    dialog.set_element(new_element(datafile, element_values))
    dialog.get_element().set_record_id(3456)
    # dialog is changed,
    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Yes
    assert dialog.action_cancel(save_something, 0)

    dialog = Dialog(main, datafile, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
    dialog.form = DummyForm(dialog)
    dialog.set_element(new_element(datafile, element_values))
    dialog.get_element().set_record_id(-5)
    # dialog is changed,
    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Yes
    assert not dialog.action_cancel(save_something, 0)
    datafile_close(datafile)


def test_09_12_set_combo_box_selections(filesystem, qtbot):
    dialog, main, datafile = base_setup(filesystem, qtbot)
    dialog.form = DummyForm(dialog)
    ids = ["1", "3", "7", "10", "15", "60"]
    entry = "7"
    dialog.set_combo_box_selections(dialog.form.combo_box, ids, entry)
    assert dialog.form.combo_box.currentIndex() == ids.index(entry)
    assert dialog.form.combo_box.currentText() == entry
    assert dialog.form.combo_box.count() == len(ids)

    dialog.set_combo_box_selections(dialog.form.combo_box, ids)
    assert dialog.form.combo_box.currentIndex() == -1
    assert dialog.form.combo_box.currentText() == ""
    assert dialog.form.combo_box.count() == len(ids)
    datafile_close(datafile)


def test_09_13_get_set_operation(filesystem, qtbot):
    dialog, main, datafile = base_setup(filesystem, qtbot)
    assert dialog.get_operation() == Dialog.VIEW_ELEMENT
    dialog.set_operation(Dialog.ADD_ELEMENT)
    assert dialog.get_operation() == Dialog.ADD_ELEMENT
    dialog = Dialog(main, datafile, Dialog.EDIT_ELEMENT)
    assert dialog.get_operation() == Dialog.EDIT_ELEMENT
    dialog.set_operation(10)
    assert dialog.get_operation() == Dialog.VIEW_ELEMENT
    datafile_close(datafile)


def test_09_13_update_error_flag(filesystem, qtbot):
    dialog, main, datafile = base_setup(filesystem, qtbot)

    dialog.form = DummyForm(dialog)
    assert dialog.error_count == 0

    dialog.form.line_edit.set_error_frame(dialog.form.edit_error_frame)

    result = {"entry": "", "valid": False, "msg": "Must have Entry"}
    current_tooltip = dialog.form.line_edit.toolTip()
    dialog.update_error_flag(
        result,
        dialog.form.line_edit,
        dialog.form.line_edit.toolTip(),
    )
    assert dialog.form.line_edit.toolTip() == result["msg"] + "; " + current_tooltip
    assert dialog.error_count == 1
    assert dialog.form.line_edit.error

    result = {"entry": "abc", "valid": True, "msg": "Must have Entry"}
    current_tooltip = dialog.form.line_edit.toolTip()
    dialog.update_error_flag(
        result,
        dialog.form.line_edit,
        dialog.form.line_edit.toolTip(),
    )
    assert dialog.form.line_edit.toolTip() == current_tooltip
    assert dialog.error_count == 0
    assert not dialog.form.line_edit.error


def test_09_14_validate_dialog_entry(filesystem, qtbot):
    dialog, main, datafile = base_setup(filesystem, qtbot)

    dialog.form = DummyForm(dialog)
    dialog.form.line_edit.set_error_frame(dialog.form.edit_error_frame)
    dialog.form.combo_box.set_error_frame(dialog.form.combo_error_frame)
    assert dialog.error_count == 0
    dialog.form.line_edit.setToolTip("LineEdit tooltip")
    dialog.form.combo_box.setToolTip("combo_box tootltip")

    element = better_element(datafile, element_values)

    dialog.form.line_edit.setText(test_string)
    result = dialog.validate_dialog_entry(
        element.set_remarks,
        dialog.form.line_edit,
        dialog.form.line_edit.toolTip(),
    )
    assert result["valid"]
    assert result["entry"] == test_string
    assert dialog.error_count == 0
    assert result["msg"] == ""
    assert dialog.form.line_edit.toolTip() == "LineEdit tooltip"

    dialog.form.line_edit.setText(long_string)
    result = dialog.validate_dialog_entry(
        element.set_remarks,
        dialog.form.line_edit,
        dialog.form.line_edit.toolTip(),
    )
    assert not result["valid"]
    assert result["entry"] == long_string
    assert dialog.error_count == 1

    dialog.set_combo_box_selections(dialog.form.combo_box, ["1", "3", "5", "7"])
    dialog.error_count = 0
    dialog.form.combo_box.setCurrentText("2")
    result = dialog.validate_dialog_entry(
        element.set_record_id,
        dialog.form.combo_box,
        dialog.form.combo_box.toolTip(),
    )
    assert not result["valid"]
    assert result["entry"] == ""
    assert dialog.error_count == 1

    dialog.form.combo_box.setCurrentText("3")
    result = dialog.validate_dialog_entry(
        element.set_record_id,
        dialog.form.combo_box,
        dialog.form.combo_box.toolTip(),
    )
    assert result["valid"]
    assert result["entry"] == 3
    assert dialog.error_count == 0
