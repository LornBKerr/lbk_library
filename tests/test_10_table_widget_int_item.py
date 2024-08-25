"""
Test the TableWidgetIntItem class.

File:       test_10_table_widget_int_item.py
Author:     Lorn B Kerr
Copyright:  (c) 20243 Lorn B Kerr
License:    MIT, see file LICENSE
"""

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem

from lbk_library.gui import TableWidgetIntItem


def test_10_01_constructor():
    widget_value = 10
    int_table_widget = TableWidgetIntItem(widget_value)
    assert isinstance(int_table_widget, QTableWidgetItem)
    assert int_table_widget.data(Qt.ItemDataRole.DisplayRole) == str(widget_value)
    assert int_table_widget.type() == 1001


def test_10_02_less_thane():
    role = Qt.ItemDataRole.DisplayRole
    test_list = []
    widget_1 = TableWidgetIntItem(10)
    widget_2 = TableWidgetIntItem(20)
    widget_3 = TableWidgetIntItem(15)

    test_list.append(widget_1)
    test_list.append(widget_2)
    test_list.append(widget_3)

    test_list.sort()
    assert test_list[0] == widget_1
    assert test_list[1] == widget_3
    assert test_list[2] == widget_2
