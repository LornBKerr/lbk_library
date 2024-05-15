"""
Test the LineEdit class.

File:       test_09_line_edit.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

from PyQt5.QtWidgets import QLineEdit
from pytestqt import qtbot

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)


from lbk_library.gui import ErrorFrame, LineEdit


def test_01_class_type(qtbot):
    box = LineEdit()
    qtbot.addWidget(box)
    assert isinstance(box, LineEdit)
    assert isinstance(box, QLineEdit)


def test_02_focus_lost(qtbot):
    box = LineEdit()

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
    qtbot.waitSignal(box.editingFinished)


def test_03_set_error_frame(qtbot):
    box = LineEdit()
    qtbot.addWidget(box)
    assert not box.error_frame
    box.set_error_frame(ErrorFrame())
    assert isinstance(box.error_frame, ErrorFrame)


def test_04_error_property(qtbot):
    box = LineEdit()
    box.set_error_frame(ErrorFrame())
    qtbot.addWidget(box)
    assert not box._error
    assert not box.error

    box.error = True
    assert box.error

    box.error = False
    assert not box.error
    assert not box._error
