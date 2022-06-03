# command --> pytest --cov-report term-missing --cov=lbk_library ../tests/


import os
import sys

import pytest

if "/home/larry/development/lbk_library/src" not in sys.path:
    sys.path.append("/home/larry/development/lbk_library/src")

from lbk_library import Dbal, Element, Validate

database = "./test.db"


def close_database(dbref):
    dbref.sql_close()


def delete_database():
    os.remove(database)


@pytest.fixture
def open_database():
    dbref = Dbal()
    dbref.sql_connect(database)
    return dbref


@pytest.fixture
def create_table(open_database):
    dbref = open_database
    dbref.sql_query("DROP TABLE IF EXISTS 'elements'")
    create_table = (
        'CREATE TABLE IF NOT EXISTS "elements"'
        + '("entry_index" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,'
        + ' "remarks" TEXT DEFAULT NULL)'
    )
    dbref.sql_query(create_table)
    return dbref


# set element values from array of values
element_values = {
    "entry_index": 9876,
    "remarks": "test",
}

# Initialize 'elements' table
def test_01_new_database(create_table):
    dbref = create_table
    assert dbref.sql_is_connected()
    close_database(dbref)


# end test_01_new_database()


def test_02_element_constr(open_database):
    dbref = open_database
    element = Element(dbref, "elements")
    assert isinstance(element, Element)
    close_database(dbref)


# end test_02_element_constr()


def test_03_element_get_dbref(open_database):
    dbref = open_database
    element = Element(dbref, "elements")
    assert element.get_dbref() == dbref
    close_database(dbref)


# end test_03_element_get_dbref()


def test_04_element_get_table(open_database):
    dbref = open_database
    element = Element(dbref, "elements")
    assert element.get_table() == "elements"
    close_database(dbref)


# end test_04_element_get_table()


def test_05_element_get_validate(open_database):
    dbref = open_database
    element = Element(dbref, "elements")
    assert isinstance(element._validate, Validate)
    close_database(dbref)


# end test_05_element_get_validate()


def test_06_element_get_set_initial_values(open_database):
    dbref = open_database
    element = Element(dbref, "elements")
    initial_values = element.get_initial_values()  # start with default values
    assert isinstance(initial_values, dict)
    assert len(initial_values) == len(element._defaults)
    element.set_initial_values(element_values)
    initial_values = element.get_initial_values()
    assert isinstance(initial_values, dict)
    assert len(initial_values) == len(element_values)
    for key in element_values:
        assert initial_values[key] == element_values[key]
    try:
        element.set_initial_values(10)
    except Exception as excp:
        assert isinstance(excp, TypeError)
    close_database(dbref)


def test_07_element_set_default_values_constructor(open_database):
    dbref = open_database
    element = Element(dbref, "elements", element_values)
    initial_values = element.get_initial_values()
    assert isinstance(initial_values, dict)
    assert len(initial_values) == len(element_values)
    for key in element_values:
        assert initial_values[key] == element_values[key]
    try:
        element.set_initial_values(10)
    except Exception as excp:
        assert isinstance(excp, TypeError)
    close_database(dbref)


def test_08_value_changed_flags(open_database):
    dbref = open_database
    element = Element(dbref, "elements")
    element.set_initial_values(element_values)
    assert not element.have_values_changed()
    element.set_value_changed_flag("entry_index", element_values["entry_index"])
    assert not element.have_values_changed()
    element.set_value_changed_flag("entry_index", element_values["entry_index"] + 1)
    assert element.have_values_changed()
    element.clear_value_changed_flags()
    assert not element.have_values_changed()
    close_database(dbref)


def test_09_get_set_properties_valid_flags(open_database):
    dbref = open_database
    element = Element(dbref, "elements")
    assert not element.set_value_valid_flag("entry_index", False)
    assert not element.get_value_valid_flag("entry_index")
    assert element.set_value_valid_flag("remarks", True)
    assert element.get_value_valid_flag("remarks")
    close_database(dbref)


def test_10_element_get_properties(open_database, create_table):
    dbref = open_database
    element = Element(dbref, "elements")
    assert isinstance(element.get_properties(), dict)
    assert len(element.get_properties()) == 0
    close_database(dbref)


def test_11_get_set_indiv_properties(open_database):
    dbref = open_database
    element = Element(dbref, "elements")
    with pytest.raises(KeyError) as exc_info:
        # Fails because no property values set yet.
        value = element._get_property("entry_index")
    exc_raised = exc_info.value
    assert exc_info.typename == "KeyError"
    element._set_property("entry_index", 10)
    assert isinstance(element.get_properties(), dict)
    assert len(element.get_properties()) == 1
    assert element._get_property("entry_index") == 10
    element._set_property("remarks", "remark 1")
    assert isinstance(element.get_properties(), dict)
    assert len(element.get_properties()) == 2
    assert element._get_property("remarks") == "remark 1"
    assert element.get_properties()["entry_index"] == 10
    assert element.get_properties()["remarks"] == "remark 1"
    close_database(dbref)


def test_12_is_element_valid(open_database):
    dbref = open_database
    element = Element(dbref, "elements")
    assert not element.is_element_valid()  # should be false because nothing is set
    element._set_property("entry_index", 10)
    # bad key
    with pytest.raises(KeyError) as exc_info:
        # not assigned so should raise KeyError
        value = element.is_element_valid()
    exc_raised = exc_info.value
    assert exc_info.typename == "KeyError"
    element.set_value_valid_flag("entry_index", False)
    assert not element.is_element_valid()
    element.set_value_valid_flag("entry_index", True)
    assert element.is_element_valid()
    element.clear_value_valid_flags()
    with pytest.raises(KeyError) as exc_info:
        # no flags so not a valid request
        value = element.is_element_valid()
    exc_raised = exc_info.value
    assert exc_info.typename == "KeyError"
    close_database(dbref)


# end test_12_is_element_valid()


def test_13_update_property_flags(open_database):
    dbref = open_database
    element = Element(dbref, "elements", {"entry_index": 0, "remarks": ""})
    element._set_property("entry_index", 1)
    element._set_property("remarks", "")
    element.update_property_flags("entry_index", 1, True)
    element.update_property_flags("remarks", "", True)
    assert element.get_value_changed_flag("entry_index")
    assert element.have_values_changed()
    assert element.get_value_valid_flag("entry_index")
    assert element.get_value_valid_flag("remarks")
    assert element.is_element_valid()
    element.update_property_flags("entry_index", 0, False)
    assert not element.get_value_changed_flag("entry_index")
    assert not element.have_values_changed()
    assert not element.get_value_valid_flag("entry_index")
    assert not element.is_element_valid()
    # bad key
    with pytest.raises(KeyError) as exc_info:
        # not assigned so should raise KeyError
        value = element.get_value_changed_flag("bad_key")
    exc_raised = exc_info.value
    assert exc_info.typename == "KeyError"
    close_database(dbref)


def test_14_named_get_value(open_database):
    dbref = open_database
    element = Element(dbref, "elements")
    with pytest.raises(KeyError) as exc_info:
        # not assigned so should raise KeyError
        value = element.get_entry_index()
    exc_raised = exc_info.value
    assert exc_info.typename == "KeyError"
    with pytest.raises(KeyError) as exc_info:
        # not assigned so should raise KeyError
        value = element.get_remarks()
    exc_raised = exc_info.value
    assert exc_info.typename == "KeyError"

    element._set_property("entry_index", None)
    assert element.get_entry_index() == 0
    element._set_property("remarks", None)
    assert element.get_remarks() == ""

    element._set_property("entry_index", 10)
    assert element.get_entry_index() == 10
    element._set_property("remarks", "remark 1")
    assert element.get_remarks() == "remark 1"
    close_database(dbref)


def test_15_set_functions(open_database):
    dbref = open_database
    element = Element(dbref, "elements", {"entry_index": 0, "remarks": ""})
    # set element properties from 'element_values'
    #'entry_index': 9876, required
    result = element.set_entry_index(None)
    assert not result["valid"]
    assert result["entry"] == None
    result = element.set_entry_index(-1)
    assert not result["valid"]
    result = element.set_entry_index(element_values["entry_index"])
    assert result["valid"]
    assert result["entry"] == element_values["entry_index"]
    assert result["entry"] == element.get_entry_index()
    # 'remarks': 'test', not required
    result = element.set_remarks(None)
    assert result["valid"]
    assert result["entry"] == ""
    result = element.set_remarks(element_values["remarks"])
    assert result["valid"]
    assert result["entry"] == element_values["remarks"]
    assert result["entry"] == element.get_remarks()
    # remarks: fail for non-text parameter
    result = element.set_remarks(100)
    assert not result["valid"]
    close_database(dbref)


def test_16_element_set_properties(open_database):
    dbref = open_database
    element = Element(dbref, "elements", {"entry_index": 0, "remarks": ""})
    element.set_properties(element_values)
    assert len(element.get_properties()) == 2
    assert element.get_entry_index() == element_values["entry_index"]
    assert element.get_remarks() == element_values["remarks"]
    close_database(dbref)


def test_17_element_add(create_table):
    dbref = create_table
    element = Element(dbref, "elements")
    element.set_initial_values({"entry_index": 0, "remarks": ""})
    element.set_properties(element_values)
    element_id = element.add()
    assert element_id == 1
    assert element_id == element.get_entry_index()
    assert element_values["remarks"] == element.get_remarks()
    close_database(dbref)


def test_18_element_read_db(create_table):
    dbref = create_table
    element = Element(dbref, "elements", {"entry_index": 0, "remarks": ""})
    element.set_properties(element_values)
    element_id = element.add()
    assert element_id == 1
    # read db for existing element
    element2 = Element(dbref, "elements", {"entry_index": 0, "remarks": ""})
    element2.get_properties_from_db("entry_index", 1)
    assert element2.get_properties() is not None
    assert element2.get_entry_index() == 1
    assert element_values["remarks"] == element2.get_remarks()
    # read db for non-existing element
    element3 = Element(dbref, "elements", {"entry_index": 0, "remarks": ""})
    element3.get_properties_from_db("entry_index", 5)
    assert isinstance(element3.get_properties(), dict)
    assert len(element3.get_properties()) == 0
    # Try direct read thru Element
    element2.set_properties(element2.get_properties_from_db(None, None))
    assert not element2.get_properties()
    close_database(dbref)


def test_19_element_update(create_table):
    dbref = create_table
    element = Element(dbref, "elements")
    element.set_initial_values({"entry_index": 0, "remarks": ""})
    element.set_properties(element_values)
    element_id = element.add()
    assert element_id == 1
    assert element_values["remarks"] == element.get_remarks()
    # update element remarks
    remarks = "these are updated remarks"
    element.set_remarks(remarks)
    result = element.update()
    assert result
    assert element.get_properties() is not None
    assert element.get_entry_index() == 1
    assert remarks == element.get_remarks()
    close_database(dbref)


def test_20_element_delete(create_table):
    dbref = create_table
    element = Element(dbref, "elements", {"entry_index": 0, "remarks": ""})
    element.set_properties(element_values)
    element_id = element.add()
    assert element_id == 1
    assert element_values["remarks"] == element.get_remarks()
    # delete element
    result = element.delete()
    assert result
    # make sure it is really gone
    element2 = Element(dbref, "elements")
    element2.get_properties_from_db("entry_index", 1)
    assert len(element2.get_properties()) == 0
    close_database(dbref)


def test_20_cleanup(open_database):
    dbref = open_database
    result = dbref.sql_query("DROP TABLE IF EXISTS 'elements'")
    assert result
    close_database(dbref)
    delete_database()


# end lbk_library_03_element.py
