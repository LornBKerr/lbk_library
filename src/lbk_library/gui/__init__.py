"""
The Project Library Collection.

This contains a set of common classes that support several projects.

This package contains the following classes:
    ComboBox extends QComboBox - Emits the 'activate' signal when
        the focus is lost.
    Dialog extends QDialog - Base class for various dialogs used
        in projects.
    ErrorFrame extends QFrame - Provides a red border around a dialog
        member to indicate an error.
    LineEdit extends QLineEdit - Emits the 'editingFinished' signal when
        the focus is lost.
    RowState -Enumerates the various states a table row may have.
    TableComboBox - Encapsules a ComboBox and an ErrorFrame into a
        widget to place in a QtableWidget row.
    TableLineEdit - Encapsules a LineEdit and an ErrorFrame into a
        widget to place in a QtableWidget row.

File:       __init__.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file LICENSE
"""

from .combo_box import ComboBox
from .dialog import Dialog
from .error_frame import ErrorFrame
from .line_edit import LineEdit
from .row_state import RowState
from .table_combo_box import TableComboBox
from .table_line_edit import TableLineEdit
