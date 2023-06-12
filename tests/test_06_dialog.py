"""
Test the Dialog class.

File:       test_06_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from PyQt6.QtWidgets import QComboBox, QDialog, QMainWindow, QMessageBox
from pytestqt import qtbot

# from pytestqt.qt_compat import qt_api


src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from test_setup import (
    A_Form,
    better_element,
    db_close,
    db_create,
    db_open,
    element_values,
    new_element,
    save_something,
)

from lbk_library import Dbal, Element
from lbk_library.gui import Dialog


def test_06_01_class_type(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
    assert isinstance(dialog, Dialog)
    assert isinstance(dialog, QDialog)


def test_06_02_get_dbref(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
    assert dialog.get_dbref() == dbref


def test_06_03_get_set_element(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref, Dialog.VIEW_ELEMENT)
    assert dialog.get_element() is None
    dialog.set_element(new_element(dbref))
    qtbot.addWidget(main)
    assert isinstance(dialog.get_element(), Element)
    dialog.set_element(better_element(dbref))
    assert isinstance(dialog.get_element(), Element)


def test_06_04_msg_info_close(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
    msg = "Testing Information Box"
    msg_box = dialog.message_information_close(msg)
    assert msg_box.icon() == QMessageBox.Icon.Information
    assert msg_box.windowTitle() == "Success"
    assert msg_box.text() == msg
    assert (
        msg_box.standardButtons()
        == QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )


def test_06_05_msg_quest_changed_close(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
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


def test_06_06_msg_quest_changed(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
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


def test_06_07_msg_quest_no_changes(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
    title = "Form Entries Have Not Changed"
    msg = "Nothing has changed, so nothing to save"
    msg_box = dialog.message_question_no_changes()
    assert msg_box.icon() == QMessageBox.Icon.Question
    assert msg_box.windowTitle() == title
    assert msg_box.text() == msg
    assert msg_box.standardButtons() == QMessageBox.StandardButton.Ok


def test_06_08_msg_warning_selection(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
    name = "Source"
    action = "Save"
    msg = "Nothing to "
    msg_box = dialog.message_warning_selection(name, action)
    assert msg_box.icon() == QMessageBox.Icon.Warning
    assert msg_box.windowTitle() == name + " has not been selected"
    assert msg_box.text() == msg + action
    assert msg_box.standardButtons() == QMessageBox.StandardButton.Ok


def test_06_09_msg_warning_failed(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
    operation = "Add"
    msg = "The " + operation + " operation failed for some reason."
    msg_box = dialog.message_warning_failed(operation)
    assert msg_box.icon() == QMessageBox.Icon.Warning
    assert msg_box.windowTitle() == operation + " Operation Failed"
    assert msg_box.text() == msg
    assert msg_box.standardButtons() == QMessageBox.StandardButton.Ok


def test_06_10_msg_warning_invalid(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
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


def test_06_11_set_invalid_indicator(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
    dialog.form = A_Form(dialog)
    font = dialog.form.record_id_label.font()
    weight = font.weight()
    dialog.set_invalid_indicator(dialog.form.record_id_label)
    new_font = dialog.form.record_id_label.font()
    assert new_font.bold()


def test_06_11_set_valid_indicator(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
    dialog.form = A_Form(dialog)
    dialog.set_invalid_indicator(dialog.form.record_id_label)
    font = dialog.form.record_id_label.font()
    weight = font.weight()
    dialog.set_valid_indicator(dialog.form.record_id_label)
    new_font = dialog.form.record_id_label.font()
    assert not new_font.bold()


def test_06_12_action_cancel(qtbot, mocker):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
    dialog.form = A_Form(dialog)
    dialog.set_element(new_element(dbref, element_values))
    # dialog is unchanged, just close
    assert dialog.action_cancel(save_something, 0)

    dialog = Dialog(main, dbref, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
    dialog.form = A_Form(dialog)
    dialog.set_element(new_element(dbref, element_values))
    dialog.get_element().set_record_id(3456)
    # dialog is changed,
    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.No
    assert dialog.action_cancel(save_something, 0)

    dialog = Dialog(main, dbref, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
    dialog.form = A_Form(dialog)
    dialog.set_element(new_element(dbref, element_values))
    dialog.get_element().set_record_id(3456)
    # dialog is changed,
    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Yes
    assert dialog.action_cancel(save_something, 0)

    dialog = Dialog(main, dbref, Dialog.VIEW_ELEMENT)
    qtbot.addWidget(main)
    dialog.form = A_Form(dialog)
    dialog.set_element(new_element(dbref, element_values))
    dialog.get_element().set_record_id(-5)
    # dialog is changed,
    mocker.patch.object(Dialog, "message_box_exec")
    dialog.message_box_exec.return_value = QMessageBox.StandardButton.Yes
    assert not dialog.action_cancel(save_something, 0)


def test_06_13_set_combo_box_selections(qtbot, db_create):
    dbref = db_create
    main = QMainWindow()
    dialog = Dialog(main, dbref, Dialog.VIEW_ELEMENT)
    dialog.form = A_Form(dialog)
    ids = ["1", "3", "7", "10", "15", "60"]
    entry = "7"
    dialog.set_combo_box_selections(dialog.form.record_id_combo, ids, entry)
    assert dialog.form.record_id_combo.currentIndex() == ids.index(entry)
    assert dialog.form.record_id_combo.currentText() == entry
    assert dialog.form.record_id_combo.count() == len(ids)

    dialog.set_combo_box_selections(dialog.form.record_id_combo, ids)
    assert dialog.form.record_id_combo.currentIndex() == -1
    assert dialog.form.record_id_combo.currentText() == ""
    assert dialog.form.record_id_combo.count() == len(ids)


def test_06_03_get_set_operation(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref, Dialog.VIEW_ELEMENT)
    assert dialog.get_operation() == Dialog.VIEW_ELEMENT
    dialog.set_operation(Dialog.ADD_ELEMENT)
    assert dialog.get_operation() == Dialog.ADD_ELEMENT
    dialog = Dialog(main, dbref, Dialog.EDIT_ELEMENT)
    assert dialog.get_operation() == Dialog.EDIT_ELEMENT
    dialog.set_operation(10)
    assert dialog.get_operation() == Dialog.VIEW_ELEMENT
