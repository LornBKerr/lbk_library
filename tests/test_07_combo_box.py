"""
Test the ComboBox class.

File:       test_07_07_combo_box.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from PySide6.QtWidgets import QComboBox
from pytestqt import qtbot

from lbk_library.gui import ComboBox, ErrorFrame


def test_07_01_class_type(qtbot):
    box = ComboBox()
    qtbot.addWidget(box)
    assert isinstance(box, ComboBox)
    assert isinstance(box, QComboBox)


def test_07_02_focus_lost(qtbot):
    box = ComboBox()

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


def test_07_03_set_frame(qtbot):
    box = ComboBox()
    qtbot.addWidget(box)
    assert not box.error_frame
    box.set_error_frame(ErrorFrame())
    assert isinstance(box.error_frame, ErrorFrame)


def test_07_04_error_property(qtbot):
    box = ComboBox()
    box.set_frame(ErrorFrame())
    qtbot.addWidget(box)
    assert not box._error
    assert not box.error

    box.error = True
    assert box.error

    box.error = False
    assert not box.error
    assert not box._error
