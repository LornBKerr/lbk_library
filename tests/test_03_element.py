"""
Tests for the Element Class.

File:       test_03_element.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file LICENSE
"""

import os
import sys

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

import pytest
from test_setup import (
    datafile_definition,
    datafile_name,
    datafile_table,
    element_values,
)

from lbk_library import DataFile, Element, Validate
from lbk_library.testing_support.core_setup import (
    datafile_close,
    datafile_create,
    datafile_open,
    directories,
    filesystem,
)


def base_setup(tmp_path):
    base_directory = filesystem(tmp_path)
    filename = base_directory + "/" + datafile_name
    datafile = datafile_create(filename, datafile_definition)
    element = Element(datafile, datafile_table)
    return (element, datafile)


def test_03_01_element_constr(tmp_path):
    element, datafile = base_setup(tmp_path)
    assert isinstance(element, Element)
    datafile_close(datafile)


def test_03_02_element_get_datafile(tmp_path):
    element, datafile = base_setup(tmp_path)
    assert element.get_datafile() == datafile
    datafile_close(datafile)


def test_03_03_element_get_table(tmp_path):
    element, datafile = base_setup(tmp_path)
    element = Element(datafile, "elements")
    assert element.get_table() == "elements"
    datafile_close(datafile)


def test_03_04_element_get_validate(tmp_path):
    element, datafile = base_setup(tmp_path)
    assert isinstance(element.validate, Validate)
    datafile_close(datafile)


def test_03_05_element_get_set_initial_values(tmp_path):
    element, datafile = base_setup(tmp_path)
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
    datafile_close(datafile)


def test_03_06_element_set_default_values_constructor(tmp_path):
    element, datafile = base_setup(tmp_path)
    element = Element(datafile, "elements", element_values)
    initial_values = element.get_initial_values()
    assert isinstance(initial_values, dict)
    assert len(initial_values) == len(element_values)
    for key in element_values:
        assert initial_values[key] == element_values[key]
    try:
        element.set_initial_values(10)
    except Exception as excp:
        assert isinstance(excp, TypeError)
    datafile_close(datafile)


def test_03_07_value_changed_flags(tmp_path):
    element, datafile = base_setup(tmp_path)
    element.set_initial_values(element_values)
    assert not element.have_values_changed()
    element.set_value_changed_flag("record_id", element_values["record_id"])
    assert not element.have_values_changed()
    element.set_value_changed_flag("record_id", element_values["record_id"] + 1)
    assert element.have_values_changed()
    element.clear_value_changed_flags()
    assert not element.have_values_changed()
    datafile_close(datafile)


def test_03_08_get_set_properties_valid_flags(tmp_path):
    element, datafile = base_setup(tmp_path)
    assert not element.set_value_valid_flag("record_id", False)
    assert not element.get_value_valid_flag("record_id")
    assert element.set_value_valid_flag("remarks", True)
    assert element.get_value_valid_flag("remarks")
    datafile_close(datafile)


def test_03_09_element_get_properties(tmp_path):
    element, datafile = base_setup(tmp_path)
    assert isinstance(element.get_properties(), dict)
    assert len(element.get_properties()) == 0
    datafile_close(datafile)


def test_03_10_get_set_indiv_properties(tmp_path):
    element, datafile = base_setup(tmp_path)
    with pytest.raises(KeyError) as exc_info:
        # Fails because no property values set yet.
        value = element._get_property("record_id")
    exc_raised = exc_info.value
    assert exc_info.typename == "KeyError"
    element._set_property("record_id", 10)
    assert isinstance(element.get_properties(), dict)
    assert len(element.get_properties()) == 1
    assert element._get_property("record_id") == 10
    element._set_property("remarks", "remark 1")
    assert isinstance(element.get_properties(), dict)
    assert len(element.get_properties()) == 2
    assert element._get_property("remarks") == "remark 1"
    assert element.get_properties()["record_id"] == 10
    assert element.get_properties()["remarks"] == "remark 1"
    datafile_close(datafile)


def test_03_11_is_element_valid(tmp_path):
    element, datafile = base_setup(tmp_path)
    assert not element.is_element_valid()  # should be false because nothing is set
    element._set_property("record_id", 10)
    # bad key
    with pytest.raises(KeyError) as exc_info:
        # not assigned so should raise KeyError
        value = element.is_element_valid()
    exc_raised = exc_info.value
    assert exc_info.typename == "KeyError"
    element.set_value_valid_flag("record_id", False)
    assert not element.is_element_valid()
    element.set_value_valid_flag("record_id", True)
    assert element.is_element_valid()
    element.clear_value_valid_flags()
    with pytest.raises(KeyError) as exc_info:
        # no flags so not a valid request
        value = element.is_element_valid()
    exc_raised = exc_info.value
    assert exc_info.typename == "KeyError"
    datafile_close(datafile)


def test_03_12_update_property_flags(tmp_path):
    element, datafile = base_setup(tmp_path)
    element = Element(datafile, "elements", {"record_id": 0, "remarks": ""})
    element._set_property("record_id", 1)
    element._set_property("remarks", "")
    element.update_property_flags("record_id", 1, True)
    element.update_property_flags("remarks", "", True)
    assert element.get_value_changed_flag("record_id")
    assert element.have_values_changed()
    assert element.get_value_valid_flag("record_id")
    assert element.get_value_valid_flag("remarks")
    assert element.is_element_valid()
    element.update_property_flags("record_id", 0, False)
    assert not element.get_value_changed_flag("record_id")
    assert not element.have_values_changed()
    assert not element.get_value_valid_flag("record_id")
    assert not element.is_element_valid()
    # bad key
    with pytest.raises(KeyError) as exc_info:
        # not assigned so should raise KeyError
        value = element.get_value_changed_flag("bad_key")
    exc_raised = exc_info.value
    assert exc_info.typename == "KeyError"
    datafile_close(datafile)


def test_03_13_named_get_value(tmp_path):
    element, datafile = base_setup(tmp_path)
    with pytest.raises(KeyError) as exc_info:
        # not assigned so should raise KeyError
        value = element.get_record_id()
    exc_raised = exc_info.value
    assert exc_info.typename == "KeyError"
    with pytest.raises(KeyError) as exc_info:
        # not assigned so should raise KeyError
        value = element.get_remarks()
    exc_raised = exc_info.value
    assert exc_info.typename == "KeyError"

    element._set_property("record_id", None)
    assert element.get_record_id() == 0
    element._set_property("remarks", None)
    assert element.get_remarks() == ""

    element._set_property("record_id", 10)
    assert element.get_record_id() == 10
    element._set_property("remarks", "remark 1")
    assert element.get_remarks() == "remark 1"
    datafile_close(datafile)


def test_03_14_set_functions(tmp_path):
    element, datafile = base_setup(tmp_path)
    element = Element(datafile, "elements", {"record_id": 0, "remarks": ""})
    # set element properties from 'element_values'
    #'record_id': 9876, required
    result = element.set_record_id(None)
    assert not result["valid"]
    assert result["entry"] == None
    result = element.set_record_id(-1)
    assert not result["valid"]
    result = element.set_record_id(element_values["record_id"])
    assert result["valid"]
    assert result["entry"] == element_values["record_id"]
    assert result["entry"] == element.get_record_id()
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
    datafile_close(datafile)


def test_03_15_element_set_properties(tmp_path):
    element, datafile = base_setup(tmp_path)
    element = Element(datafile, "elements", {"record_id": 0, "remarks": ""})
    set_results = element.set_properties(element_values)
    assert len(element.get_properties()) == 2
    assert element.get_record_id() == element_values["record_id"]
    assert element.get_remarks() == element_values["remarks"]
    assert len(set_results) == 2
    assert set_results["record_id"]["entry"] == element_values["record_id"]
    assert set_results["record_id"]["valid"] == True
    assert set_results["record_id"]["msg"] == ""
    datafile_close(datafile)


def test_03_16_element_add(tmp_path):
    element, datafile = base_setup(tmp_path)
    element = Element(datafile, "elements", {"record_id": 0, "remarks": ""})
    element.set_initial_values({"record_id": 0, "remarks": ""})
    element.set_properties(element_values)
    element_id = element.add()
    assert element_id == 1
    assert element_id == element.get_record_id()
    assert element_values["remarks"] == element.get_remarks()
    datafile_close(datafile)


def test_03_17_element_read_db(tmp_path):
    element, datafile = base_setup(tmp_path)
    element = Element(datafile, "elements", {"record_id": 0, "remarks": ""})
    element.set_properties(element_values)
    element_id = element.add()
    assert element_id == 1
    # read db for existing element
    element2 = Element(datafile, "elements", {"record_id": 0, "remarks": ""})
    element2.get_properties_from_datafile("record_id", 1)
    assert element2.get_properties() is not None
    assert element2.get_record_id() == 1
    assert element_values["remarks"] == element2.get_remarks()
    # read db for non-existing element
    element3 = Element(datafile, "elements", {"record_id": 0, "remarks": ""})
    element3.get_properties_from_datafile("record_id", 5)
    assert isinstance(element3.get_properties(), dict)
    assert len(element3.get_properties()) == 0
    # Try direct read thru Element
    element2.set_properties(element2.get_properties_from_datafile(None, None))
    assert not element2.get_properties()
    datafile_close(datafile)


def test_03_18_element_update(tmp_path):
    element, datafile = base_setup(tmp_path)
    element = Element(datafile, "elements")
    element.set_initial_values({"record_id": 0, "remarks": ""})
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
    assert element.get_record_id() == 1
    assert remarks == element.get_remarks()
    datafile_close(datafile)


def test_03_19_element_delete(tmp_path):
    element, datafile = base_setup(tmp_path)
    element = Element(datafile, "elements", {"record_id": 0, "remarks": ""})
    element.set_properties(element_values)
    element_id = element.add()
    assert element_id == 1
    assert element_values["remarks"] == element.get_remarks()
    # delete element
    result = element.delete()
    assert result
    # make sure it is really gone
    element2 = Element(datafile, "elements")
    element2.get_properties_from_datafile("record_id", 1)
    assert len(element2.get_properties()) == 0
    datafile_close(datafile)


def test_03_20_set_validated_property(tmp_path):
    element, datafile = base_setup(tmp_path)
    element = Element(datafile, "elements")
    element.set_validated_property("test", True, "is_valid", "not_valid")
    assert element._get_property("test") == "is_valid"
    assert element._get_property("test") != "not_valid"
    element.set_validated_property("test", False, "is_valid", "not_valid")
    assert element._get_property("test") != "is_valid"
    assert element._get_property("test") == "not_valid"
