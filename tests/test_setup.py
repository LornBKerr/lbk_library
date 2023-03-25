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

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import Dbal, Element

db_name = "test.db"


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
    dbref = Dbal()
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
