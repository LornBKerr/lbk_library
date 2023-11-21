"""
The Project Library Collection.

This contains a set of common classes that support several projects.

This package contains the following classes:
    Dbal           A database abstraction layer for SQLite3.
    Element        Base class for types of information in a database.
    ElementSet     Base class for a set of elements.
    IniFileParser  Read and Write *.ini Files
    Validate       Support validation of values going into the database.

    gui.ComboBox extends QComboBox - Emits the 'activate' signal when
        the focus is lost.
    gui.Dialog extends QDialog - Base class for various dialogs used in
        projects.
    gui.ErrorFrame extends QFrame - Provides a red border around a dialog
        member to indicate an error.
    gui.LineEdit extends QLineEdit - Emits the 'editingFinished' signal
        when the focus is lost.
    gui.RowState - Enumerates the various states a table row may have.
    gui.TableButtonGroup - Contains a group of TablePushButtons.
    gui.TableComboBox - Encapsules a ComboBox and an ErrorFrame into a
        widget to place in a QtableWidget row.
    gui.TableLineEdit - Encapsules a LineEdit and an ErrorFrame into a
        widget to place in a QtableWidget row.
    gui.TablePushButton - Extends a QPushButton to be used in a Table.

File:       __init__.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    see License
"""

from .dbal import Dbal
from .element import Element
from .element_set import ElementSet
from .gui import (
    ComboBox,
    Dialog,
    ErrorFrame,
    LineEdit,
    RowState,
    TableButtonGroup,
    TableComboBox,
    TableLineEdit,
    TablePushButton,
)
from .ini_file_parser import IniFileParser
from .validate import Validate
