"""
Test the FocusComboBox class.

File:       test_07_focus>combo_box.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from PyQt5.QtWidgets import QComboBox
from pytestqt import qtbot

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)


from lbk_library.gui.focus_combo_box import FocusComboBox


def test_01_class_type(qtbot):
    box = FocusComboBox()
    qtbot.addWidget(box)
    assert isinstance(box, FocusComboBox)
    assert isinstance(box, QComboBox)


def test_02_focus_lost(qtbot):
    box = FocusComboBox()

    def got_focus():
        assert box.hasFocus()

    qtbot.addWidget(box)
    box.show()

    # set the focus combo box to have focus (setFocus())
    box.setFocus()

    # unset the focus (clearFocus())
    qtbot.waitUntil(got_focus)

    # check that the focusOut event is handled.
    box.clearFocus()
    qtbot.waitSignal(box.activated)
