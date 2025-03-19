"""
Test the TableModel class.

File:       test_11_table_model.py
Author:     Lorn B Kerr
Copyright:  (c) 2024 Lorn B Kerr
License:    MIT, see file LICENSE
"""

import os
import sys
from copy import deepcopy

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from PySide6.QtCore import QAbstractTableModel, Qt  # QModelIndex,
from PySide6.QtGui import QBrush, QColor
from test_setup import datafile_name

from lbk_library.gui import CellData, TableModel
from lbk_library.testing_support import (
    datafile_close,
    datafile_create,
    filesystem,
    load_datafile_table,
)

header_names = ["Record Id", "Name", "Species", "Tank Number"]

tool_tips = ["Tool Tip 0", "Tool Tip 1", "Tool Tip 2", "Tool Tip 3"]

cell_alignments = [
    Qt.AlignmentFlag.AlignLeft,
    Qt.AlignmentFlag.AlignHCenter,
    Qt.AlignmentFlag.AlignRight,
    Qt.AlignmentFlag.AlignLeft,
]

normal_background = QBrush(QColor("white"))
error_background = QBrush(QColor("red"))

column_names = ["record_id", "name", "species", "tank_number"]

test_value_set = [
    [1, "Sammy", "shark", 1],
    [2, "Jamie", "cuttlefish", 7],
]

datafile_definition = [
    (
        'CREATE TABLE IF NOT EXISTS "fish"'
        '("record_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,'
        ' "name" TEXT DEFAULT NULL,'
        ' "species" TEXT DEFAULT NULL,'
        ' "tank_number" INTEGER)'
    ),
]


def setup_table_model(qtbot, tmp_path):
    base_directory = filesystem(tmp_path)
    filename = base_directory + datafile_name
    datafile = datafile_create(filename, datafile_definition)
    load_datafile_table(datafile, "fish", column_names, test_value_set)
    model = TableModel(
        deepcopy(test_value_set),
        header_names,
        tool_tips,
        cell_alignments,
        normal_background,
    )
    return (datafile, model)


def test_11_01_class_type(qtbot, tmp_path):
    datafile, model = setup_table_model(qtbot, tmp_path)

    assert isinstance(model, TableModel)
    assert isinstance(model, QAbstractTableModel)
    assert len(model._data_set) == len(test_value_set)
    for row in range(len(test_value_set)):
        for column in range(len(test_value_set[0])):
            assert model._data_set[row][column].value == test_value_set[row][column]
            assert model._data_set[row][column].alignment == cell_alignments[column]
            assert model._data_set[row][column].background == normal_background
            assert model._data_set[row][column].tooltip == tool_tips[column]

    datafile_close(datafile)


def test_11_02_rowCount(qtbot, tmp_path):
    datafile, model = setup_table_model(qtbot, tmp_path)

    assert model.rowCount() == len(test_value_set)
    datafile_close(datafile)


def test_11_03_columnCount(qtbot, tmp_path):
    datafile, model = setup_table_model(qtbot, tmp_path)

    assert model.columnCount() == len(header_names)
    datafile_close(datafile)


def test_11_04_flags(qtbot, tmp_path):
    datafile, model = setup_table_model(qtbot, tmp_path)

    for row in range(model.rowCount()):
        for column in range(model.columnCount()):
            flags = model.flags(model.index(row, column))
            assert flags & Qt.ItemFlag.ItemIsSelectable
            assert flags & Qt.ItemFlag.ItemIsEnabled
            if column != header_names.index("Record Id"):
                assert flags & Qt.ItemFlag.ItemIsEditable
    datafile_close(datafile)


def test_11_05_header_data(qtbot, tmp_path):
    datafile, model = setup_table_model(qtbot, tmp_path)

    for column in range(model.columnCount()):
        assert (
            model.headerData(column, Qt.Orientation.Horizontal)
            == model._header_titles[column]
        )
    datafile_close(datafile)


def test_11_06_setHeaderData(qtbot, tmp_path):
    datafile, model = setup_table_model(qtbot, tmp_path)

    def action_header_changed(orientation, first_column, second_column):
        assert orientation == Qt.Orientation.Horizontal
        assert first_column == column
        assert second_column == column

    column = 1
    model.headerDataChanged.connect(action_header_changed)
    new_value = "New Header"
    success = model.setHeaderData(column, Qt.Orientation.Horizontal, new_value)
    assert success
    assert model.headerData(column, Qt.Orientation.Horizontal) == new_value
    datafile_close(datafile)


def test_11_07_insert_rows(qtbot, tmp_path):
    datafile, model = setup_table_model(qtbot, tmp_path)

    current_rows = model.rowCount()
    success = model.insertRows(1, 2)
    assert model.rowCount() == current_rows + 2
    assert success
    datafile_close(datafile)


def test_11_08_remove_rows(qtbot, tmp_path):
    datafile, model = setup_table_model(qtbot, tmp_path)

    model.insertRows(1, 2)
    current_rows = model.rowCount()
    assert isinstance(model._data_set[1][0], CellData)
    assert isinstance(model._data_set[2][0], CellData)
    assert not model._data_set[3][0].value == None

    success = model.removeRows(1, 1)
    assert model.rowCount() == current_rows - 1
    assert model._data_set[1][0].value == None
    assert not model._data_set[2][0].value == None
    assert success
    datafile_close(datafile)


def test_11_09_data(qtbot, tmp_path):
    datafile, model = setup_table_model(qtbot, tmp_path)

    # If table has more columns than data has, should return None
    assert (
        model.data(
            model.createIndex(0, len(model._data_set[0])),
            Qt.ItemDataRole.DisplayRole,
        )
        == None
    )

    for row in range(model.rowCount()):
        for column in range(len(model._data_set[0])):
            index = model.createIndex(row, column)
            assert (
                model.data(index, Qt.ItemDataRole.DisplayRole)
                == test_value_set[row][column]
            )
            assert (
                model.data(index, Qt.ItemDataRole.EditRole)
                == test_value_set[row][column]
            )
            assert model.data(index, Qt.ItemDataRole.ToolTipRole) == tool_tips[column]
            assert model.data(index, Qt.ItemDataRole.BackgroundRole) == QBrush(
                QColor("White")
            )
            assert (
                model.data(index, Qt.ItemDataRole.TextAlignmentRole)
                == cell_alignments[column]
            )

    datafile_close(datafile)


def test_11_10_setData(qtbot, tmp_path):
    datafile, model = setup_table_model(qtbot, tmp_path)

    def action_data_changed(a_index, b_index):
        assert a_index.row() == b_index.row()
        assert a_index.row() == myindex.row()
        assert a_index.column() == b_index.column()
        assert a_index.column() == myindex.column()

    model.dataChanged.connect(action_data_changed)
    new_value = 25

    # requested column greater than number of data columns.
    myindex = model.createIndex(0, len(header_names))
    assert model.setData(myindex, new_value, Qt.ItemDataRole.EditRole)
    assert model.data(myindex) is None

    #  column valid, change edit value in column and row.
    myindex = model.createIndex(0, 0)
    model.setData(myindex, new_value, Qt.ItemDataRole.EditRole)
    assert model.data(myindex) == new_value

    #  column valid, change display value in column and row.
    myindex = model.createIndex(1, 0)
    model.setData(myindex, new_value, Qt.ItemDataRole.DisplayRole)
    assert model.data(myindex) == new_value

    # set a  tooltip
    new_tooltip = "A new tooltip"
    model.setData(myindex, new_tooltip, Qt.ItemDataRole.ToolTipRole)
    assert model.data(myindex, Qt.ItemDataRole.ToolTipRole) == new_tooltip

    # set a non default background
    assert model.data(myindex, Qt.ItemDataRole.BackgroundRole) == normal_background
    new_background = QBrush(QColor("Green"))
    assert model.setData(myindex, new_background, Qt.ItemDataRole.BackgroundRole)
    assert model.data(myindex, Qt.ItemDataRole.BackgroundRole) == new_background

    # set an alignment
    assert model.data(myindex, Qt.ItemDataRole.TextAlignmentRole) == cell_alignments[0]
    new_alignment = cell_alignments[1]
    assert model.setData(myindex, new_alignment, Qt.ItemDataRole.TextAlignmentRole)
    assert model.data(myindex, Qt.ItemDataRole.TextAlignmentRole) == cell_alignments[1]
