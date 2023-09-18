"""
The Project Library Collection.

This contains a set of common classes that support several projects.

This package contains the following classes:
    Dbal           A database abstraction layer for SQLite3.
    Element        Base class for types of information in a database.
    ElementSet     Base class for a set of elements.
    IniFileParser  Read and Write *.ini Files
    Validate       Support validation of values going into the database.

    gui.Dialog          Base class for various dialogs used in projects.
    gui.FocusComboBox   Extend QComboBox to emit the activate signal when
                        the focus is lost.

File:       __init__.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    see License
"""

from .dbal import Dbal
from .element import Element
from .element_set import ElementSet
from .gui import Dialog, ErrorFrame, ComboBox, LineEdit
from .ini_file_parser import IniFileParser
from .validate import Validate
