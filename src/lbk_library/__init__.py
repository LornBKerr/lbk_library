"""
The Project Library Collection.

This contains two packages and a set of a set of common classes that
support several projects.

The set of common classes provide a group of commonly used abstractions.
    DataFile       Implement a DataFile for permanent storage of information.
    Element        Base class for types of information in the datafile.
    ElementSet     Base class for sets of elements.
    IniFileParser  Read and Write *.ini Files (Deprecated in favor of
        Qt.QtCore.QSettings.
    Validate       Support validation of values going into the database.

File:       __init__.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2024 Lorn B Kerr
License:    see License
License:    MIT, see file LICENSE
"""

from .datafile import DataFile
from .element import Element
from .element_set import ElementSet
from .ini_file_parser import IniFileParser
from .testing_support import core_setup
from .validate import Validate

file_version = "1.1.0"
changes = {
    "1.0.0": "Initial release",
    "1.1.0": "Changed name from 'Dbal' to 'DataFile'.",
}
