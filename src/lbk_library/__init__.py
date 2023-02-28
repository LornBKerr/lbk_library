"""
The Project Library Collection.

This contains a set of common classes that support several projects.

This package contains the following classes:
    Dbal           A database abstraction layer for SQLite3.
    Element        Base class for types of information in a database.
    ElementSet     Base class for a set of elements.
    IniFileParser  Read and Write *.ini Files
    Validate       Support validation of values going into the database.

Sub-packages for GUI support will be added as sibling projects require.

File:       __init__.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    see License
"""

from .dbal import Dbal
from .element import Element
from .element_set import ElementSet

# from .gui.dialog import Dialog
# from .gui.focus_combo_box import FocusComboBox
from .ini_file_parser import IniFileParser
from .validate import Validate


def version():
    """Return the current version of the library."""
    from setuptools_scm import get_version

    return get_version()
