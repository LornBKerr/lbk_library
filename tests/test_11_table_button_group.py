"""
Test the TablePushgroup class.

File:       test_11_table_button_group.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from PyQt5.QtWidgets import QFrame, QTableWidget
from pytestqt import qtbot

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)


from lbk_library.gui import TableButtonGroup, TablePushButton

# group Id Constants
EDIT_SAVE = 16
DELETE = 32

# Number of table rows
row_0 = 0
row_3 = 3

col_0 = 0
col_3 = 3


def test_01_class_type(qtbot):
    table = QTableWidget(None)
    group = TableButtonGroup(table, row_0, col_0)
    qtbot.addWidget(group)
    assert isinstance(group, TableButtonGroup)
    assert isinstance(group, QFrame)


def test_02_properties(qtbot):
    table = QTableWidget(None)
    group = TableButtonGroup(table, row_0, col_3)
    qtbot.addWidget(group)
    assert group.table == table
    assert group.row == row_0
    assert group.column == col_3


def test_03_add_button(qtbot):
    table = QTableWidget(None)
    group = TableButtonGroup(table, row_0, col_0)
    qtbot.addWidget(group)
    assert isinstance(group.buttons, dict)
    assert len(group.buttons) == 0

    new_button = group.add_button("Edit", EDIT_SAVE)
    assert len(group.buttons) == 1
    assert group.buttons[EDIT_SAVE]
