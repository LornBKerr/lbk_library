"""
The Project Library Collection.

This contains two packages and a set of a set of common classes that
support several projects.

The set of common classes provide a group of commonly used abstractions.
    DataFile       Implement a DataFile for permanent storage of information.
    Element        Base class for types of information in the datafile.
    ElementSet     Base class for sets of elements.
    IniFileParser  Read and Write *.ini Files (Deprecated in favor of 
        Qt.QtCore.QSettings
    Validate       Support validation of values going into the database.

The included sub -packages support handling forms and common test
functionallity.
    gui             extendes the basic some Qt standard classes adding 
        specific actions or combining seversl classes.
    testing_support provides a number of values and functions to help
        setup thegeneral test environment for different projects. All 
        test modules draw on a varying selection of these values.

File:       __init__.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    see License
"""

from .datafile import DataFile
from .element import Element
from .element_set import ElementSet
from .gui import ComboBox, Dialog, ErrorFrame, LineEdit
from .ini_file_parser import IniFileParser
from .testing_support import core_setup
from .validate import Validate
