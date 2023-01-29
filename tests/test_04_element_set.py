# command --> pytest --cov-report term-missing --cov=lbk_library ../tests/

import os
import sys

import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from lbk_library import Dbal, Element, ElementSet, Validate

database = "test.db"
table_name = "elements"


def close_database(dbref):
    dbref.sql_close()


def new_element(dbref, properties={}):
    # create a new Element from properties
    element = Element(dbref, table_name)
    element.set_initial_values(properties)
    element.set_properties(properties)
    element.clear_value_changed_flags()
    return element


@pytest.fixture
def open_database(tmpdir):
    path = tmpdir.join(database)
    dbref = Dbal()
    # valid connection
    dbref.sql_connect(path)
    return dbref


@pytest.fixture
def create_table(open_database):
    dbref = open_database
    dbref.sql_query("DROP TABLE IF EXISTS " + table_name)
    create_table = (
        "CREATE TABLE IF NOT EXISTS "
        + table_name
        + '("record_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,'
        + ' "remarks" TEXT DEFAULT NULL)'
    )
    dbref.sql_query(create_table)
    return dbref


def test_04_01_ElementSet_constr(create_table):
    dbref = create_table
    element_set = ElementSet(dbref, table_name, Element)
    assert isinstance(element_set, ElementSet)
    close_database(dbref)


def test_04_02_ElementSet_get_dbref(create_table):
    dbref = create_table
    element_set = ElementSet(dbref, table_name, Element)
    assert element_set.get_dbref() == dbref
    close_database(dbref)


def test_04_03_ElementSet_get_table(create_table):
    dbref = create_table
    element_set = ElementSet(dbref, table_name, Element)
    assert element_set.get_table() == table_name
    close_database(dbref)


def test_04_04_ElementSet_set_table(create_table):
    dbref = create_table
    element_set = ElementSet(dbref, table_name, Element)
    element_set.set_table("parts")
    assert element_set.get_table() == "parts"
    close_database(dbref)


def test_04_05_ElementSet_get_properties_type(create_table):
    dbref = create_table
    element_set = ElementSet(dbref, table_name, Element)
    element_set.set_property_set(None)
    prop_set = element_set.get_property_set()
    assert isinstance(prop_set, list)
    assert len(prop_set) == 0
    close_database(dbref)


def test_04_06_Element_set_constructor(create_table):
    dbref = create_table
    remark = "Remark # "
    element_values = {"record_id": 1, "remarks": remark}
    for i in range(5):  # put 5 entries in the table
        element_values["remarks"] = remark + str(5 - i)
        element = new_element(dbref, element_values)
        element_id = element.add()

    element_set = ElementSet(dbref, table_name, Element)
    properties = element_set.get_property_set()
    assert len(properties) == 5
    for i in range(5):
        element = properties[i]
        assert element.get_record_id() == i + 1
    assert element_set.get_number_elements() == len(properties)

    # text_element_set_constructor_columns
    element_set = ElementSet(dbref, table_name, Element, "record_id", 3)
    properties = element_set.get_property_set()
    assert len(properties) == 1
    assert isinstance(properties, list)
    assert properties[0].get_record_id() == 3

    # order by clause
    element_set = ElementSet(dbref, table_name, Element, None, None, "remarks")
    properties = element_set.get_property_set()
    for i in range(5):
        assert properties[i].get_remarks() == "Remark # " + str(i + 1)
    element_set = ElementSet(dbref, table_name, Element, None, None, "record_id")
    properties = element_set.get_property_set()
    for i in range(5):
        assert properties[i].get_remarks() == "Remark # " + str(5 - i)

        # limits and offset
    element_set = ElementSet(dbref, table_name, Element, None, None, None, 3)
    properties = element_set.get_property_set()
    assert element_set.get_number_elements() == 3
    element_set = ElementSet(dbref, table_name, Element, None, None, None, 3, 1)
    properties = element_set.get_property_set()
    assert element_set.get_number_elements() == 3
    assert properties[0].get_record_id() == 2
    close_database(dbref)


def test_04_07_insert_element(create_table):
    dbref = create_table
    remark = "Remark # "
    element_values = {"record_id": 1, "remarks": remark}
    for i in range(5):  # put 5 entries in the table
        element_values["remarks"] = remark + str(5 - i)
        element = new_element(dbref, element_values)
        element_id = element.add()
    element_set = ElementSet(dbref, table_name, Element)
    length = element_set.get_number_elements()
    assert length == len(element_set.get_property_set())
    new_values = {"record_id": 0, "remarks": "Remark # 6"}
    element = new_element(dbref, new_values)
    element_set.insert(length, element)
    assert length + 1 == len(element_set.get_property_set())
    assert element_set.get_property_set()[length].get_remarks() == "Remark # 6"
    close_database(dbref)


def test_04_08_append_element(create_table):
    dbref = create_table
    remark = "Remark # "
    element_values = {"record_id": 1, "remarks": remark}
    for i in range(5):  # put 5 entries in the table
        element_values["remarks"] = remark + str(5 - i)
        element = new_element(dbref, element_values)
        element_id = element.add()
    element_set = ElementSet(dbref, table_name, Element)
    length = element_set.get_number_elements()
    assert length == len(element_set.get_property_set())
    new_values = {"record_id": 0, "remarks": "Remark # 6"}
    element = new_element(dbref, new_values)
    element_set.append(element)
    assert length + 1 == len(element_set.get_property_set())
    assert element_set.get_property_set()[length].get_remarks() == "Remark # 6"
    close_database(dbref)


def test_04_09_get_element(create_table):
    dbref = create_table
    remark = "Remark # "
    element_values = {"record_id": 1, "remarks": remark}
    for i in range(5):  # put 5 entries in the table
        element_values["remarks"] = remark + str(5 - i)
        element = new_element(dbref, element_values)
        element_id = element.add()
    element_set = ElementSet(dbref, table_name, Element)
    length = element_set.get_number_elements()
    assert length == len(element_set.get_property_set())
    third_element_index = 2
    third_element = element_set.get(third_element_index)
    assert third_element.get_record_id() == 3
    close_database(dbref)


def test_04_10_delete_element(create_table):
    dbref = create_table
    length = 5
    remark = "Remark # "
    element_values = {"record_id": 1, "remarks": remark}
    for i in range(length):  # put 5 entries in the table
        element_values["remarks"] = remark + str(5 - i)
        element = new_element(dbref, element_values)
        element_id = element.add()
    element_set = ElementSet(dbref, table_name, Element)
    assert length == len(element_set.get_property_set())
    third_element_index = 2
    element_set.delete(third_element_index)
    new_set = element_set.get_property_set()
    assert len(new_set) == length - 1
    assert new_set[third_element_index].get_record_id() == 4
    close_database(dbref)


def test_04_11_build_option_list(create_table):
    dbref = create_table
    remark = "Remark # "
    element_values = {"record_id": 1, "remarks": remark}
    number_elements = 5
    for i in range(number_elements):  # put 5 entries in the table
        element_values["remarks"] = remark + str(5 - i)
        element = new_element(dbref, element_values)
        element_id = element.add()
    element_set = ElementSet(dbref, table_name, Element)
    properties = element_set.get_property_set()
    assert len(properties) == number_elements
    # build an option list
    option_list = element_set.build_option_list("record_id")
    assert len(option_list) == 5
    i = 1
    for record_id in option_list:
        assert record_id == str(i)
        i += 1
    close_database(dbref)


def test_04_12_iterator(create_table):
    dbref = create_table
    element = Element(dbref, table_name)
    remark = "Remark # "
    element_values = {"record_id": 1, "remarks": remark}
    for i in range(5):  # put 5 entries in the table
        element_values["remarks"] = remark + str(5 - i)
        element.set_initial_values(element_values)
        element.set_properties(element_values)
        element_id = element.add()
    element_set = ElementSet(dbref, table_name, Element)
    i = 1
    for row in element_set:
        assert row.get_record_id() == i
        i += 1
    close_database(dbref)


# end test_04_ElementSet.py
