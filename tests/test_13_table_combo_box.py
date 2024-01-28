"""
Test the ComboBox class.

File:       test_13_table_combo_box.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from PyQt5.QtWidgets import QTableWidget, QWidget

# from pytestqt import qtbot

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library.gui import ComboBox, ErrorFrame, TableComboBox

# Number of table rows
rows = 4
row_0 = 0
row_3 = 3

cols = 4
col_0 = 0
col_3 = 3

selections = ["102-150", "13062", "17001"]


def test_01_class_type(qtbot):
    table = QTableWidget(rows, cols)
    box = TableComboBox(table, row_0, col_0, selections)
    qtbot.addWidget(box)
    box.show()
    assert isinstance(box, TableComboBox)
    assert isinstance(box, QWidget)


def test_02_properties(qtbot):
    table = QTableWidget(rows, cols)
    box = TableComboBox(table, row_0, col_0, selections)
    qtbot.addWidget(box)
    assert box.table == table
    assert box.row == row_0
    box.row = row_3
    assert box.row == row_3
    assert box.column == row_0
    box.column = col_3
    assert box.column == col_3
    assert isinstance(box.error_frame, ErrorFrame)


def test_03_cell_changed(qtbot):
    table = QTableWidget(rows, cols)
    box = TableComboBox(table, row_3, col_3, selections)
    qtbot.addWidget(box)

    def cell_changed(row, column):
        assert row == row_3
        assert column == col_3

    table.cellChanged.connect(cell_changed)
    box.combo_box.activated.emit(box.currentIndex())


def test_04_set_get_current_text(qtbot):
    table = QTableWidget(rows, cols)
    box = TableComboBox(table, row_0, col_0, selections)
    qtbot.addWidget(box)

    box.setCurrentText(selections[0])
    assert box.combo_box.currentText() == selections[0]
    assert box.currentText() == selections[0]


def test_05_set_get_current_index(qtbot):
    table = QTableWidget(rows, cols)
    box = TableComboBox(table, row_0, col_0, selections)
    qtbot.addWidget(box)

    box.setCurrentIndex(0)
    assert box.combo_box.currentIndex() == 0
    assert box.currentText() == selections[0]
    assert box.currentIndex() == 0


def test_06_error_property(qtbot):
    table = QTableWidget(rows, cols)
    box = TableComboBox(table, row_0, col_0, selections)
    qtbot.addWidget(box)

    assert not box.error
    assert not box.combo_box.error

    box.error = True
    assert box.error
    assert box.combo_box.error

    box.error = False
    assert not box.error
