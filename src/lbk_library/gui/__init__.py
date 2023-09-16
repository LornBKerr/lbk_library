"""
The Project Library Collection.

This contains a set of common classes that support several projects.

This package contains the following classes:
    Dialog extends QDialog - Base class for various dialogs used in projects.
    ErrorFrame extends QFrame
    FocusComboBox extend QComboBox - emits the 'activate' signal when
        the focus is lost.
    LineEdit extends QLineEdit - Emits the 'editingFinished' signal when
        the focus is lost.

File:       __init__.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file LICENSE
"""

from .dialog import Dialog
from .error_frame import ErrorFrame
from .focus_combo_box import FocusComboBox
from .line_edit import LineEdit
