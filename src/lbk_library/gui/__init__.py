"""
The Project Library Collection Gui Package.

This package extendes the basic some Qt standard classes adding specific
actions or combining seversl classes.

This package contains the following modules:
    ComboBox extends QComboBox - Emits the 'activate' signal when
        the focus is lost.
    ComboBoxDelegate extends QStyledItemDelegate - Provides a QComboBox
        for use in QTableView objects.
    Dialog extends QDialog - Base class for various dialogs used
        in projects.
    ErrorFrame extends QFrame - Provides a red border around a dialog
        member to indicate an error.
    LineEdit extends QLineEdit - Emits the 'editingFinished' signal when
        the focus is lost.
    Settings extends QSettings -Adds functionality to set and retrieve 
        Lists as one-line calls.
    TableModel extends QAbstractTableModel - Provides access to 
        QTableView derived tables.
    TableWidgetIntItem extends QTableWidgetItem - Adds the capability of
        sorting a table on an column of integers.

File:       __init__.py
Author:     Lorn B Kerr
Copyright:  (c) 2023, 2025 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    1.1.0
"""

from .combo_box import ComboBox
from .dialog import Dialog
from .error_frame import ErrorFrame
from .line_edit import LineEdit
from .settings import Settings
from .table_model import CellData, TableModel
from .table_widget_int_item import TableWidgetIntItem

file_version = "1.0.1"
changes = {
    "1.0.0": "Initial release",
    "1.0.1": "Added Version Info",
    "1.1.0": "Added TableModel and Settings to the set of classes."
}
