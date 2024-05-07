"""
Test setup for the lbk_library functionality.

File:       test_setup.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
"""

import os
import sys

import pytest
from PyQt5 import QtCore, QtWidgets

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import DataFile, Element

db_name = "library_test.db"


sql_statements = [
    (
        'CREATE TABLE IF NOT EXISTS "elements"'
        '("record_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,'
        ' "remarks" TEXT DEFAULT NULL,'
        ' "installed" BOOLEAN)'
    ),
]


@pytest.fixture
def db_open(tmpdir):
    path = tmpdir.join(db_name)
    dbref = DataFile()
    dbref.sql_connect(path)
    return dbref


def db_close(dbref):
    dbref.sql_close()


@pytest.fixture
def db_create(db_open):
    dbref = db_open
    for sql in sql_statements:
        dbref.sql_query(sql)
    return dbref


# set element values from array of values
element_values = {
    "record_id": 9876,
    "remarks": "test",
}


def new_element(dbref, properties={}):
    # create a new Element from properties
    element = Element(dbref, "elements")
    element.set_initial_values(properties)
    element.set_properties(properties)
    element.clear_value_changed_flags()
    return element


def better_element(dbref, properties={}):
    # create a new Element from properties
    better_element = Element(dbref, "elements")
    better_element.set_initial_values(properties)
    better_element.set_properties(properties)
    better_element.clear_value_changed_flags()
    return better_element


# define a do nothing function to act as the 'save_action' parameter of
# the dialog,action_cancel() function.
def save_something(action):
    pass


# define a simple form with various qt objects aavailable for testing.
class A_Form(object):
    def __init__(self, A_Form):
        self.setupUi(A_Form)

    def setupUi(self, dialog_form):
        """Initialize comment."""
        dialog_form.setObjectName("dialog_form")
        dialog_form.resize(910, 580)
        self.record_id_label = QtWidgets.QLabel(parent=dialog_form)
        self.record_id_label.setGeometry(QtCore.QRect(5, 30, 125, 36))
        self.record_id_combo = QtWidgets.QComboBox(parent=dialog_form)
        self.record_id_combo.setGeometry(QtCore.QRect(140, 30, 161, 36))
        self.remarks_label = QtWidgets.QLabel(parent=dialog_form)
        self.remarks_label.setGeometry(QtCore.QRect(5, 260, 125, 37))
        self.remarks_edit = QtWidgets.QLineEdit(parent=dialog_form)
        self.remarks_edit.setGeometry(QtCore.QRect(140, 260, 271, 37))
