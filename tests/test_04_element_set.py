"""
Tests for the ElementSet Class.

File:       test_03_element_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file LICENSE
"""

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from test_setup import (
    datafile_definition,
    datafile_name,
    element_definition,
    new_element,
)

from lbk_library import DataFile, Element, ElementSet
from lbk_library.testing_support.core_setup import (
    datafile_close,
    datafile_create,
    directories,
    filesystem,
)


def base_setup(tmp_path):
    base_directory = filesystem(tmp_path)
    filename = base_directory + "/" + datafile_name
    datafile = datafile_create(filename, datafile_definition)
    element_set = ElementSet(datafile, "elements", Element)
    print(type(element_set))
    return (filename, datafile, element_set)


def test_04_01_ElementSet_constr(tmp_path):
    filename, datafile, element_set = base_setup(tmp_path)
    #    datafile = DataFile()
    #    element_set = ElementSet(datafile, "elements", Element)
    assert isinstance(element_set, ElementSet)
    datafile_close(datafile)


def test_04_02_ElementSet_get_datafile(tmp_path):
    filename, datafile, element_set = base_setup(tmp_path)
    assert element_set.get_datafile() == datafile
    datafile_close(datafile)


def test_04_03_ElementSet_get_table(tmp_path):
    filename, datafile, element_set = base_setup(tmp_path)
    assert element_set.get_table() == "elements"
    datafile_close(datafile)


def test_04_04_ElementSet_set_table(tmp_path):
    filename, datafile, element_set = base_setup(tmp_path)
    element_set.set_table("parts")
    assert element_set.get_table() == "parts"
    datafile_close(datafile)


def test_04_05_ElementSet_get_properties_type(tmp_path):
    filename, datafile, element_set = base_setup(tmp_path)
    element_set.set_property_set(None)
    prop_set = element_set.get_property_set()
    assert isinstance(prop_set, list)
    assert len(prop_set) == 0
    datafile_close(datafile)


def test_04_06_ElementSet_constructor(tmp_path):
    filename, datafile, element_set = base_setup(tmp_path)
    remark = "Remark # "
    element_values = {"record_id": None, "remarks": remark}
    for i in range(5):  # put 5 entries in the table
        element_values["remarks"] = remark + str(5 - i)
        element = new_element(datafile, element_values)
        element_id = element.add()

    element_set = ElementSet(datafile, "elements", Element)
    properties = element_set.get_property_set()
    assert len(properties) == 5
    for i in range(5):
        element = properties[i]
        assert element.get_record_id() == i + 1
    assert element_set.get_number_elements() == len(properties)

    # text_element_set_constructor_columns
    element_set = ElementSet(datafile, "elements", Element, "record_id", 3)
    properties = element_set.get_property_set()
    assert len(properties) == 1
    assert isinstance(properties, list)
    assert properties[0].get_record_id() == 3

    # order by clause
    element_set = ElementSet(datafile, "elements", Element, None, None, "remarks")
    properties = element_set.get_property_set()
    for i in range(5):
        assert properties[i].get_remarks() == "Remark # " + str(i + 1)
    element_set = ElementSet(datafile, "elements", Element, None, None, "record_id")
    properties = element_set.get_property_set()
    for i in range(5):
        assert properties[i].get_remarks() == "Remark # " + str(5 - i)

        # limits and offset
    element_set = ElementSet(datafile, "elements", Element, None, None, None, 3)
    properties = element_set.get_property_set()
    assert element_set.get_number_elements() == 3
    element_set = ElementSet(datafile, "elements", Element, None, None, None, 3, 1)
    properties = element_set.get_property_set()
    assert element_set.get_number_elements() == 3
    assert properties[0].get_record_id() == 2
    datafile_close(datafile)


def test_04_07_insert_element(tmp_path):
    filename, datafile, element_set = base_setup(tmp_path)
    remark = "Remark # "
    element_values = {"record_id": 1, "remarks": remark}
    for i in range(5):  # put 5 entries in the table
        element_values["remarks"] = remark + str(5 - i)
        element = new_element(datafile, element_values)
        element_id = element.add()
    element_set = ElementSet(datafile, "elements", Element)
    length = element_set.get_number_elements()
    assert length == len(element_set.get_property_set())
    new_values = {"record_id": 0, "remarks": "Remark # 6"}
    element = new_element(datafile, new_values)
    element_set.insert(length, element)
    assert length + 1 == len(element_set.get_property_set())
    assert element_set.get_property_set()[length].get_remarks() == "Remark # 6"
    datafile_close(datafile)


def test_04_08_append_element(tmp_path):
    filename, datafile, element_set = base_setup(tmp_path)
    remark = "Remark # "
    element_values = {"record_id": None, "remarks": remark}
    for i in range(5):  # put 5 entries in the table
        element_values["remarks"] = remark + str(5 - i)
        element = new_element(datafile, element_values)
        element_id = element.add()
    element_set = ElementSet(datafile, "elements", Element)
    length = element_set.get_number_elements()
    assert length == len(element_set.get_property_set())
    new_values = {"record_id": None, "remarks": "Remark # 6"}
    element = new_element(datafile, new_values)
    element_set.append(element)
    assert length + 1 == len(element_set.get_property_set())
    assert element_set.get_property_set()[length].get_remarks() == "Remark # 6"
    datafile_close(datafile)


def test_04_09_get_element(tmp_path):
    filename, datafile, element_set = base_setup(tmp_path)
    remark = "Remark # "
    element_values = {"record_id": 1, "remarks": remark}
    for i in range(5):  # put 5 entries in the table
        element_values["remarks"] = remark + str(5 - i)
        element = new_element(datafile, element_values)
        element_id = element.add()
    element_set = ElementSet(datafile, "elements", Element)
    length = element_set.get_number_elements()
    assert length == len(element_set.get_property_set())
    third_element_index = 2
    third_element = element_set.get(third_element_index)
    assert third_element.get_record_id() == 3
    datafile_close(datafile)


def test_04_10_delete_element(tmp_path):
    filename, datafile, element_set = base_setup(tmp_path)
    length = 5
    remark = "Remark # "
    element_values = {"record_id": 1, "remarks": remark}
    for i in range(length):  # put 5 entries in the table
        element_values["remarks"] = remark + str(5 - i)
        element = new_element(datafile, element_values)
        element_id = element.add()
    element_set = ElementSet(datafile, "elements", Element)
    assert length == len(element_set.get_property_set())
    third_element_index = 2
    element_set.delete(third_element_index)
    new_set = element_set.get_property_set()
    assert len(new_set) == length - 1
    assert new_set[third_element_index].get_record_id() == 4
    datafile_close(datafile)


def test_04_11_build_option_list(tmp_path):
    filename, datafile, element_set = base_setup(tmp_path)
    remark = "Remark # "
    element_values = {"record_id": 1, "remarks": remark}
    number_elements = 5
    for i in range(number_elements):  # put 5 entries in the table
        element_values["remarks"] = remark + str(5 - i)
        element = new_element(datafile, element_values)
        element_id = element.add()
    element_set = ElementSet(datafile, "elements", Element)
    properties = element_set.get_property_set()
    assert len(properties) == number_elements
    # build an option list
    option_list = element_set.build_option_list("record_id")
    assert len(option_list) == 5
    i = 1
    for record_id in option_list:
        assert record_id == str(i)
        i += 1
    datafile_close(datafile)


def test_04_12_iterator(tmp_path):
    filename, datafile, element_set = base_setup(tmp_path)
    element = Element(datafile, "elements")
    remark = "Remark # "
    element_values = {"record_id": 1, "remarks": remark}
    for i in range(5):  # put 5 entries in the table
        element_values["remarks"] = remark + str(5 - i)
        element.set_initial_values(element_values)
        element.set_properties(element_values)
        element_id = element.add()
    i = 1
    element_set = ElementSet(datafile, "elements", Element)
    for row in element_set:
        assert row.get_record_id() == i
        i += 1
    datafile_close(datafile)


def test_04_13_get_type(tmp_path):
    filename, datafile, element_set = base_setup(tmp_path)
    assert element_set.get_type() == Element
