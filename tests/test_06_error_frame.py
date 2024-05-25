"""
Test the ErrorFrame class.

File:       test_06_error_frame.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from PyQt5.QtWidgets import QFrame
from pytestqt import qtbot

from lbk_library.gui.error_frame import ErrorFrame


def test_06_01_class_type(qtbot):
    frame = ErrorFrame()
    qtbot.addWidget(frame)
    assert isinstance(frame, ErrorFrame)
    assert isinstance(frame, QFrame)


def test_06_02_error_property(qtbot):
    frame = ErrorFrame()
    qtbot.addWidget(frame)
    assert not frame._error
    assert frame.styleSheet() == frame._frame_style_normal

    frame.error = True
    assert frame.error
    assert frame.styleSheet() == frame._frame_style_error

    frame.error = False
    assert not frame.error
    assert frame.styleSheet() == frame._frame_style_normal
