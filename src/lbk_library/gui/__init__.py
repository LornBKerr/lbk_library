"""
The Project Library Collection.

This contains a set of common classes that support several projects.

This package contains the following classes:
    Dialog          Base class for various dialogs used in projects.
    FocusComboBox   Extend QComboBox to emit the activate signal when
                    the focus is lost.

File:       __init__.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    see License
"""

from .dialog import Dialog
from .focus_combo_box import FocusComboBox
