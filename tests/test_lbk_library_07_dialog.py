import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from PyQt6.QtWidgets import QDialog, QMainWindow
import pytest
from pytestqt import qtbot

from lbk_library import Dbal
from lbk_library.qt.dialog import Dialog


def test_01_class_type(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref)

    qtbot.addWidget(main)
    assert isinstance(dialog, Dialog)
    assert isinstance(dialog, QDialog)


def test_02_constructor(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref)
    
    assert dialog.get_dbref() == dbref
    assert dialog.get_element() is None


    
    
