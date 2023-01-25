import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

import pytest
from PyQt6.QtWidgets import QDialog, QMainWindow
from pytestqt import qtbot

from lbk_library import Dbal, Element
from lbk_library.qt.dialog import Dialog


class NewElement(Element):
    # define a minimal element for testing purposes
    def __init__(self):
        pass


class BetterElement(Element):
    # define a minimal element for testing purposes
    def __init__(self):
        pass


def test_01_class_type(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref)
    qtbot.addWidget(main)
    assert isinstance(dialog, Dialog)
    assert isinstance(dialog, QDialog)


def test_02_get_dbref(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref)
    assert dialog.get_dbref() == dbref


def test_03_get_set_element(qtbot):
    dbref = Dbal()
    main = QMainWindow()
    dialog = Dialog(main, dbref)
    assert dialog.get_element() is None
    dialog.set_element(NewElement())
    assert isinstance(dialog.get_element(), NewElement)
    assert isinstance(dialog.get_element(), Element)
    dialog.set_element(BetterElement())
    assert isinstance(dialog.get_element(), BetterElement)
