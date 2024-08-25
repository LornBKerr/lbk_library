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

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtGui import QBrush, QColor
from test_setup import datafile_name

from lbk_library.gui import TableModel
from lbk_library.testing_support import (  # ; ;
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


def setup_table_model(qtbot, filesystem):
    filename = filesystem + "/" + datafile_name
    datafile = datafile_create(filename, datafile_definition)
    load_datafile_table(datafile, "fish", column_names, test_value_set)
    model = TableModel(
        deepcopy(test_value_set),
        header_names,
        column_names,
        tool_tips,
        cell_alignments,
    )
    return (datafile, model)


def test_11_01_class_type(qtbot, filesystem):
    datafile, model = setup_table_model(qtbot, filesystem)

    assert isinstance(model, TableModel)
    assert isinstance(model, QAbstractTableModel)
    assert len(model._data_set) == len(test_value_set)
    for i in range(len(column_names)):
        assert model._column_data_names[i] == column_names[i]
    for i in range(len(header_names)):
        assert model._header_titles[i] == header_names[i]
    assert len(model._default_column_tooltips) == len(tool_tips)
    assert model._default_column_tooltips == tool_tips
    assert isinstance(model._cell_tooltips, list)
    assert len(model._cell_tooltips) == 0
    assert model._background == QBrush(QColor("White"))
    assert model._error_background == QBrush(QColor(0xF0C0C0))
    assert isinstance(model._cell_backgrounds, list)
    assert len(model._cell_backgrounds) == 0
    assert isinstance(model._default_column_alignments, list)
    assert len(model._cell_alignments) == 0
    datafile_close(datafile)


def test_11_02_rowCount(qtbot, filesystem):
    datafile, model = setup_table_model(qtbot, filesystem)
    assert model.rowCount() == len(test_value_set)
    datafile_close(datafile)


def test_11_03_columnCount(qtbot, filesystem):
    datafile, model = setup_table_model(qtbot, filesystem)
    assert model.columnCount(QModelIndex()) == len(header_names)
    datafile_close(datafile)


def test_11_04_flags(qtbot, filesystem):
    datafile, model = setup_table_model(qtbot, filesystem)

    for row in range(model.rowCount(QModelIndex())):
        for column in range(model.columnCount(QModelIndex())):
            flags = model.flags(model.index(row, column))
            assert flags & Qt.ItemFlag.ItemIsSelectable
            assert flags & Qt.ItemFlag.ItemIsEnabled
            if column != header_names.index("Record Id"):
                assert flags & Qt.ItemFlag.ItemIsEditable
    datafile_close(datafile)


def test_11_05_header_data(qtbot, filesystem):
    datafile, model = setup_table_model(qtbot, filesystem)
    for column in range(model.columnCount(QModelIndex())):
        assert (
            model.headerData(column, Qt.Orientation.Horizontal)
            == model._header_titles[column]
        )
    datafile_close(datafile)


def test_11_06_setHeaderData(qtbot, filesystem):
    datafile, model = setup_table_model(qtbot, filesystem)

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


def test_11_07_set_default_background(qtbot, filesystem):
    datafile, model = setup_table_model(qtbot, filesystem)
    assert model._background == QBrush(QColor("White"))
    new_background = QBrush(QColor("Blue"))
    model.set_default_background(new_background)
    assert model._background == new_background
    datafile_close(datafile)


def test_11_08_set_default_error_background(qtbot, filesystem):
    datafile, model = setup_table_model(qtbot, filesystem)
    assert model._error_background == QBrush(QColor(0xF0C0C0))
    new_error_background = QBrush(QColor("Green"))
    model.set_default_error_background(new_error_background)
    assert model._error_background == new_error_background
    datafile_close(datafile)


def test_11_09_insert_rows(qtbot, filesystem):
    datafile, model = setup_table_model(qtbot, filesystem)
    current_rows = model.rowCount()
    success = model.insertRows(model.rowCount(), 2)
    assert model.rowCount() == current_rows + 2
    assert success
    datafile_close(datafile)


def test_11_10_set_default_column_alignments(qtbot, filesystem):
    datafile, model = setup_table_model(qtbot, filesystem)

    assert len(model._cell_alignments) == 0
    model.set_default_column_alignments(cell_alignments)
    assert len(model._default_column_alignments) == len(cell_alignments)
    for i in range(len(cell_alignments)):
        assert model._default_column_alignments[i] == cell_alignments[i]
    datafile_close(datafile)


def test_11_11_data_role_display_edit(qtbot, filesystem):
    datafile, model = setup_table_model(qtbot, filesystem)

    # If table has more columns than data has, should return None
    assert (
        model.data(
            model.createIndex(0, len(model._column_data_names)),
            Qt.ItemDataRole.DisplayRole,
        )
        == None
    )

    for row in range(model.rowCount()):
        for column in range(len(model._column_data_names)):
            assert (
                model.data(model.createIndex(row, column), Qt.ItemDataRole.DisplayRole)
                == test_value_set[row][column]
            )
            assert (
                model.data(model.createIndex(row, column), Qt.ItemDataRole.EditRole)
                == test_value_set[row][column]
            )
    datafile_close(datafile)


def test_11_12_data_role_tooltip(qtbot, filesystem):
    datafile, model = setup_table_model(qtbot, filesystem)

    # default tooltips
    for row in range(model.rowCount()):
        for column in range(len(model._column_data_names)):
            assert (
                model.data(model.createIndex(row, column), Qt.ItemDataRole.ToolTipRole)
                == tool_tips[column]
            )
    # cell specific tooltip in row 1, column 1.
    test_row = 1
    test_col = 1
    cell_tooltip = "error message " + tool_tips[1]
    model._cell_tooltips.append([test_row, test_col, cell_tooltip])
    assert (
        model.data(model.createIndex(test_row, test_col), Qt.ItemDataRole.ToolTipRole)
        == cell_tooltip
    )
    datafile_close(datafile)


def test_11_13_data_role_background(qtbot, filesystem):
    datafile, model = setup_table_model(qtbot, filesystem)

    for row in range(model.rowCount()):
        for column in range(len(model._column_data_names)):
            assert (
                model.data(
                    model.createIndex(row, column), Qt.ItemDataRole.BackgroundRole
                )
                == model._background
            )
    # cell specific background in row 1, column 1.
    test_row = 1
    test_col = 1
    cell_background = QBrush(QColor(0xF08080))
    model._cell_backgrounds.append([test_row, test_col, cell_background])
    assert (
        model.data(
            model.createIndex(test_row, test_col), Qt.ItemDataRole.BackgroundRole
        )
        == cell_background
    )
    datafile_close(datafile)


def test_11_14_data_role_text_alignment(qtbot, filesystem):
    datafile, model = setup_table_model(qtbot, filesystem)

    model.set_default_column_alignments(cell_alignments)
    for row in range(model.rowCount()):
        for column in range(len(model._column_data_names)):
            assert (
                model.data(
                    model.createIndex(row, column), Qt.ItemDataRole.TextAlignmentRole
                )
                == cell_alignments[column]
            )
    # cell specific alignment in row 1, column 1.
    test_row = 1
    test_col = 1
    cell_justify = Qt.AlignmentFlag.AlignJustify
    model._cell_alignments.append([test_row, test_col, cell_justify])
    assert (
        model.data(
            model.createIndex(test_row, test_col), Qt.ItemDataRole.TextAlignmentRole
        )
        == cell_justify
    )
    datafile_close(datafile)


def test_11_15_setData_role_display_edit(qtbot, filesystem):
    datafile, model = setup_table_model(qtbot, filesystem)

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
    datafile_close(datafile)


def test_11_16_setData_role_tooltip(qtbot, filesystem):
    datafile, model = setup_table_model(qtbot, filesystem)
    model._default_column_tooltips = tool_tips
    # _cell_tooltips should be empty.
    assert len(model._cell_tooltips) == 0

    # set a default tooltip
    myindex = model.createIndex(0, 0)
    model.setData(myindex, tool_tips[0], Qt.ItemDataRole.ToolTipRole)
    assert len(model._cell_tooltips) == 0
    assert model.data(myindex, Qt.ItemDataRole.ToolTipRole) == tool_tips[0]

    # set a non default tooltip
    new_tooltip = "A new tooltip"
    model.setData(myindex, new_tooltip, Qt.ItemDataRole.ToolTipRole)
    assert len(model._cell_tooltips) == 1
    assert model.data(myindex, Qt.ItemDataRole.ToolTipRole) == new_tooltip

    # set another non default tooltip
    new_tooltip = "Another new tooltip"
    model.setData(myindex, new_tooltip, Qt.ItemDataRole.ToolTipRole)
    assert len(model._cell_tooltips) == 1
    assert model.data(myindex, Qt.ItemDataRole.ToolTipRole) == new_tooltip


def test_11_17_setData_role_background(qtbot, filesystem):
    datafile, model = setup_table_model(qtbot, filesystem)
    # _cell_backgrounds should be empty.
    assert len(model._cell_backgrounds) == 0

    # set a default background
    myindex = model.createIndex(0, 0)
    model.setData(myindex, model._background, Qt.ItemDataRole.BackgroundRole)
    assert len(model._cell_backgrounds) == 0
    assert model.data(myindex, Qt.ItemDataRole.BackgroundRole) == model._background

    # set a non default background
    new_background = QBrush(QColor("Green"))
    model.setData(myindex, new_background, Qt.ItemDataRole.BackgroundRole)
    assert len(model._cell_backgrounds) == 1
    assert model.data(myindex, Qt.ItemDataRole.BackgroundRole) == new_background

    # set default error background
    new_background = model._error_background
    model.setData(myindex, new_background, Qt.ItemDataRole.BackgroundRole)
    assert len(model._cell_backgrounds) == 1
    assert model.data(myindex, Qt.ItemDataRole.BackgroundRole) == new_background


def test_11_18_setData_role_alignments(qtbot, filesystem):
    datafile, model = setup_table_model(qtbot, filesystem)
    model._default_column_alignments = cell_alignments
    # _cell_alignments should be empty.
    assert len(model._cell_alignments) == 0

    # set a default alignment
    myindex = model.createIndex(0, 0)
    model.setData(myindex, cell_alignments[0], Qt.ItemDataRole.TextAlignmentRole)
    assert len(model._cell_alignments) == 0
    assert model.data(myindex, Qt.ItemDataRole.TextAlignmentRole) == cell_alignments[0]

    # set a non default alignment
    new_alignment = Qt.AlignmentFlag.AlignJustify
    model.setData(myindex, new_alignment, Qt.ItemDataRole.TextAlignmentRole)
    assert len(model._cell_alignments) == 1
    assert model.data(myindex, Qt.ItemDataRole.TextAlignmentRole) == new_alignment

    # set another non default alignment
    new_alignment = Qt.AlignmentFlag.AlignRight
    model.setData(myindex, new_alignment, Qt.ItemDataRole.TextAlignmentRole)
    assert len(model._cell_alignments) == 1
    assert model.data(myindex, Qt.ItemDataRole.TextAlignmentRole) == new_alignment
