"""
Test the TablePushButton class.

File:       test_table_push_button.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from PyQt5.QtWidgets import QPushButton, QTableWidget
from pytestqt import qtbot

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)


from lbk_library.gui import TablePushButton

# Button Id Constants
EDIT_SAVE = 16
DELETE = 32

# Number of table rows
row_0 = 0
row_3 = 3

col_0 = 0
col_3 = 3


def test_01_class_type(qtbot):
    table = QTableWidget(None)
    button = TablePushButton(table, row_0, DELETE)
    qtbot.addWidget(button)
    assert isinstance(button, TablePushButton)
    assert isinstance(button, QPushButton)


def test_02_properties(qtbot):
    table = QTableWidget(None)
    button = TablePushButton(table, row_0, DELETE)
    qtbot.addWidget(button)
    assert button.table == table
    assert button.row == row_0
    assert button.button_id == DELETE

    table = QTableWidget(row_3, col_3, None)
    button = TablePushButton(table, row_3, EDIT_SAVE)
    assert button.table == table
    assert button.row == row_3
    assert button.button_id == EDIT_SAVE


def test_03_button_clicked(qtbot):
    def cell_clicked(row, id):
        assert row == row_0
        assert id == DELETE

    table = QTableWidget(None)
    button = TablePushButton(table, row_0, DELETE)
    qtbot.addWidget(button)
    table.cellClicked.connect(cell_clicked)

    button.show()
    button.click()
    qtbot.waitSignal(table.cellClicked)
