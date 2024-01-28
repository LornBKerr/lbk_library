"""
Test the LineEdit class.

File:       test_12_table_line_edit.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QWidget

# from pytestqt import qtbot

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)


from lbk_library.gui import ErrorFrame, LineEdit, TableLineEdit

# Number of table rows
rows = 4
row_0 = 0
row_3 = 3

cols = 4
col_0 = 0
col_3 = 3

alignment = Qt.AlignLeft | Qt.AlignVCenter


def test_01_class_type(qtbot):
    table = QTableWidget(rows, cols)
    box = TableLineEdit(table, row_0, col_0, alignment)
    qtbot.addWidget(box)
    box.show()

    assert isinstance(box, TableLineEdit)
    assert isinstance(box, QWidget)
    assert isinstance(box.error_frame, ErrorFrame)
    assert isinstance(box.line_edit, LineEdit)


def test_02_properties(qtbot):
    table = QTableWidget(rows, cols)
    box = TableLineEdit(table, row_0, col_0, alignment)
    qtbot.addWidget(box)
    assert box.row == row_0
    box.row = row_3
    assert box.row == row_3
    assert box.column == row_0
    box.column = col_3
    assert box.column == col_3


def test_03_cell_changed_signal(qtbot):
    table = QTableWidget(rows, cols)
    box = TableLineEdit(table, row_0, col_0, alignment)
    qtbot.addWidget(box)
    box.show()

    def got_focus():
        assert box.line_edit.hasFocus()

    # set the  box to have focus (setFocus())
    box.line_edit.setFocus()

    # unset the focus (clearFocus())
    qtbot.waitUntil(got_focus)

    # check that the focusOut event is handled.
    box.line_edit.clearFocus()
    qtbot.waitSignal(table.cellChanged)


def test_04_set_get_text(qtbot):
    table = QTableWidget(rows, cols)
    box = TableLineEdit(table, row_0, col_0, alignment)
    qtbot.addWidget(box)
    string = "test text"
    box.setText(string)
    assert box.text() == string


def test_05_set_read_only(qtbot):
    table = QTableWidget(rows, cols)
    box = TableLineEdit(table, row_0, col_0, alignment)
    qtbot.addWidget(box)
    assert not box.line_edit.isReadOnly()
    box.setReadOnly(True)
    assert box.line_edit.isReadOnly()
    box.setReadOnly(False)
    assert not box.line_edit.isReadOnly()


def test_06_error_property(qtbot):
    table = QTableWidget(rows, cols)
    box = TableLineEdit(table, row_0, col_0, alignment)
    qtbot.addWidget(box)

    assert not box.error
    assert not box.line_edit.error

    box.error = True
    assert box.error
    assert box.line_edit.error

    box.error = False
    assert not box.error


#
