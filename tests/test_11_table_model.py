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

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QBrush, QColor

from lbk_library.gui import CellData, TableModel
from lbk_library.testing_support.core_setup import (
    datafile_close,
    datafile_create,
    filesystem,
    load_datafile_table,
)

header_titles = ["Record Id", "Name", "Species", "Tank Number"]
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

datafile_name = "fish"


def setup_table_model(tmp_path):
    base_directory = filesystem(tmp_path)
    filename = base_directory + "/" + datafile_name
    datafile = datafile_create(filename, datafile_definition)
    load_datafile_table(datafile, "fish", column_names, test_value_set)

    model = TableModel(
        deepcopy(test_value_set),
        header_titles,
        tool_tips,
        cell_alignments,
        normal_background,
    )
    return (datafile, model)


def test_11_01_class_type(tmp_path):
    datafile, model = setup_table_model(tmp_path)

    assert isinstance(model, TableModel)
    assert isinstance(model, QAbstractTableModel)
    assert len(model.data_set) == len(test_value_set)
    for i in range(len(header_titles)):
        assert model.header_titles[i] == header_titles[i]
    assert model.background == normal_background
    datafile_close(datafile)


def test_11_02_cell_data_class(tmp_path):
    datafile, model = setup_table_model(tmp_path)

    cell_data = CellData()
    assert cell_data.value == None
    assert cell_data.alignment == None
    assert cell_data.background == None
    assert cell_data.tooltip == None

    cell_data = CellData(
        test_value_set[0][1], cell_alignments[0], error_background, tool_tips[0]
    )
    assert cell_data.value == test_value_set[0][1]
    assert cell_data.alignment == cell_alignments[0]
    assert cell_data.background == error_background
    assert cell_data.tooltip == tool_tips[0]

    datafile_close(datafile)


def test_11_03_load_cell_values(tmp_path):
    datafile, model = setup_table_model(tmp_path)

    model = TableModel(
        [],
        header_titles,
        tool_tips,
        cell_alignments,
        normal_background,
    )
    assert len(model.data_set) == 0
    model.load_cell_values(test_value_set)
    for row in range(len(test_value_set)):
        for column in range(len(test_value_set[0])):
            assert model.data_set[row][column].value == test_value_set[row][column]
            assert model.data_set[row][column].alignment == cell_alignments[column]
            assert model.data_set[row][column].background == normal_background
            assert model.data_set[row][column].tooltip == tool_tips[column]
    datafile_close(datafile)


def test_11_04_rowCount(tmp_path):
    datafile, model = setup_table_model(tmp_path)
    assert model.rowCount() == len(test_value_set)
    datafile_close(datafile)


def test_11_05_columnCount(tmp_path):
    datafile, model = setup_table_model(tmp_path)
    assert model.columnCount(QModelIndex()) == len(header_titles)
    datafile_close(datafile)


def test_11_06_flags(tmp_path):
    datafile, model = setup_table_model(tmp_path)

    for row in range(model.rowCount(QModelIndex())):
        for column in range(model.columnCount(QModelIndex())):
            flags = model.flags(model.index(row, column))
            assert flags & Qt.ItemFlag.ItemIsSelectable
            assert flags & Qt.ItemFlag.ItemIsEnabled
            if column != header_titles.index("Record Id"):
                assert flags & Qt.ItemFlag.ItemIsEditable
    datafile_close(datafile)


def test_11_07_header_data(tmp_path):
    datafile, model = setup_table_model(tmp_path)
    for column in range(model.columnCount(QModelIndex())):
        assert (
            model.headerData(column, Qt.Orientation.Horizontal)
            == model.header_titles[column]
        )
    datafile_close(datafile)


def test_11_08_setHeaderData(tmp_path):
    datafile, model = setup_table_model(tmp_path)

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


def test_11_09_insert_rows(tmp_path):
    datafile, model = setup_table_model(tmp_path)
    current_rows = model.rowCount()
    success = model.insertRows(model.rowCount(), 2)
    assert model.rowCount() == current_rows + 2
    assert success
    datafile_close(datafile)


def test_11_10_delete_rows(tmp_path):
    datafile, model = setup_table_model(tmp_path)
    current_rows = model.rowCount()
    success = model.removeRows(0, 1)
    assert model.rowCount() == current_rows - 1
    assert success
    datafile_close(datafile)


def test_11_11_data(tmp_path):
    datafile, model = setup_table_model(tmp_path)

    # If table has more columns than data has, should return None
    assert (
        model.data(
            model.createIndex(0, len(model.header_titles)),
            Qt.ItemDataRole.DisplayRole,
        )
        == None
    )

    for row in range(model.rowCount()):
        for column in range(len(model.header_titles)):
            assert (
                model.data(model.createIndex(row, column), Qt.ItemDataRole.DisplayRole)
                == test_value_set[row][column]
            )
            assert (
                model.data(model.createIndex(row, column), Qt.ItemDataRole.EditRole)
                == test_value_set[row][column]
            )
            assert (
                model.data(model.createIndex(row, column), Qt.ItemDataRole.ToolTipRole)
                == tool_tips[column]
            )
            assert (
                model.data(
                    model.createIndex(row, column), Qt.ItemDataRole.BackgroundRole
                )
                == normal_background
            )
            assert (
                model.data(
                    model.createIndex(row, column), Qt.ItemDataRole.TextAlignmentRole
                )
                == cell_alignments[column]
            )
    datafile_close(datafile)


def test_11_12_setData(tmp_path):
    datafile, model = setup_table_model(tmp_path)

    row = (0,)
    column = 1
    test_index = model.createIndex(0, 1)

    def data_changed(start_index, end_index):
        if start_index.column() == column:  # ignore out of bounds index.
            assert test_index.row() == start_index.row()
            assert test_index.column() == start_index.column()

    model.dataChanged.connect(data_changed)

    assert model.setData(model.createIndex(0, 10), "q", Qt.ItemDataRole.EditRole)

    assert model.setData(test_index, "Ralph", Qt.ItemDataRole.EditRole)
    assert model.data(test_index, Qt.ItemDataRole.EditRole) == "Ralph"

    assert model.setData(test_index, "Ralph", Qt.ItemDataRole.DisplayRole)
    assert model.data(test_index, Qt.ItemDataRole.DisplayRole) == "Ralph"

    assert model.setData(test_index, "New Tooltip", Qt.ItemDataRole.ToolTipRole)
    assert model.data(test_index, Qt.ItemDataRole.ToolTipRole) == "New Tooltip"

    assert model.setData(test_index, QColor("magenta"), Qt.ItemDataRole.BackgroundRole)
    assert model.data(test_index, Qt.ItemDataRole.BackgroundRole) == QColor("magenta")

    assert model.setData(
        test_index, Qt.AlignmentFlag.AlignRight, Qt.ItemDataRole.TextAlignmentRole
    )
    assert (
        model.data(test_index, Qt.ItemDataRole.TextAlignmentRole)
        == Qt.AlignmentFlag.AlignRight
    )
    datafile_close(datafile)
