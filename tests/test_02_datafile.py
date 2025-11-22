"""
Tests for the DataFile Class.

File:       test_02_datafile.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file LICENSE
"""

import os
import sqlite3
import sys

import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from test_setup import datafile_definition, datafile_name

from lbk_library import DataFile
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
    data_file = datafile_create(filename, datafile_definition)
    return (filename, data_file)


def test_02_01_datafile_constructor():
    data_file = DataFile()
    assert isinstance(data_file, DataFile)
    data_file.sql_close()


def test_02_02_sql_connect_invalid():
    data_file = DataFile()
    # invalid connection because of invalid path
    connection = data_file.sql_connect("./invalid_path/nn.db")
    assert not connection
    data_file.sql_close()


def test_02_03_sql_connect_valid(tmp_path):
    filename, data_file = base_setup(tmp_path)
    data_file.sql_connect(filename)
    assert data_file.sql_is_connected()
    datafile_close(data_file)
    data_file.sql_close()


def test_02_04_sql_close(tmp_path):
    filename, data_file = base_setup(tmp_path)
    assert data_file.sql_is_connected()
    data_file.sql_close()
    assert not data_file.sql_is_connected()


def test_02_05_sql_bad_statement(tmp_path):
    filename, datafile = base_setup(tmp_path)
    with pytest.raises(sqlite3.Error) as exc_info:
        sql = "SELECT * FROM"  # missing table name
        result = datafile.sql_query(sql)
    exc_raised = exc_info.value
    assert exc_info.typename == "OperationalError"
    datafile_close(datafile)


def test_02_06_sql_validate_value_none(tmp_path):
    filename, datafile = base_setup(tmp_path)
    result = datafile.sql_validate_value(None)
    assert result is None
    datafile_close(datafile)


def test_02_07_sql_validate_value_bool(tmp_path):
    filename, datafile = base_setup(tmp_path)
    result = datafile.sql_validate_value(True)
    assert isinstance(result, int)
    assert result == 1
    result = datafile.sql_validate_value(False)
    assert isinstance(result, int)
    assert result == 0
    datafile_close(datafile)


def test_02_08_sql_validate_value_string(tmp_path):
    filename, datafile = base_setup(tmp_path)
    result = datafile.sql_validate_value("a string")
    assert isinstance(result, str)
    assert result == "'a string'"
    datafile_close(datafile)


def test_02_09_sql_nextid_none(tmp_path):
    filename, datafile = base_setup(tmp_path)
    result = datafile.sql_nextid(None)
    assert result == 0
    datafile_close(datafile)


def test_02_10_sql_validate(tmp_path):
    filename, datafile = base_setup(tmp_path)
    assert datafile.sql_validate_value(None) is None
    assert datafile.sql_validate_value("test") == "'test'"
    assert datafile.sql_validate_value(10) == 10
    assert datafile.sql_validate_value(True) == 1
    assert datafile.sql_validate_value(False) == 0
    datafile_close(datafile)


def test_02_11_sql_fetchrow_none(tmp_path):
    filename, datafile = base_setup(tmp_path)
    result = datafile.sql_fetchrow(None)
    assert not result
    datafile_close(datafile)


def test_02_12_sql_fetchrowset_none(tmp_path):
    filename, datafile = base_setup(tmp_path)
    result = datafile.sql_fetchrowset(None)
    assert len(result) == 0
    datafile_close(datafile)


def test_02_13_sql_query_from_array_none(tmp_path):
    filename, datafile = base_setup(tmp_path)
    assert datafile
    result = datafile.sql_query_from_array(None)
    assert result == ""
    datafile_close(datafile)


def test_02_14_sql_query_from_array_bad_query(tmp_path):
    filename, datafile = base_setup(tmp_path)
    query = list()
    result = datafile.sql_query_from_array(query)
    assert not result
    datafile_close(datafile)


def test_02_15_sql_query_from_array_bad_type(tmp_path):
    filename, datafile = base_setup(tmp_path)
    query = {"type": "GiveMe"}
    assert not datafile.sql_query_from_array(query)
    datafile_close(datafile)


def test_02_16_sql_query_from_array_delete(tmp_path):
    filename, datafile = base_setup(tmp_path)
    value_set = {
        "record_id": None,
        "installed": False,
        "remarks": "another iffy remark",
    }
    query = {"type": "insert", "table": "elements"}
    sql_insert = datafile.sql_query_from_array(query, value_set)
    assert (
        sql_insert
        == "INSERT INTO elements (record_id, installed, remarks) VALUES (:record_id, :installed, :remarks)"
    )
    result = datafile.sql_query(sql_insert, value_set)
    assert isinstance(result, sqlite3.Cursor)
    index = datafile.sql_nextid(result)
    assert index == 1

    # good delete
    query = {"type": "delete", "table": "elements"}
    query["where"] = "record_id = " + str(index)
    sql_delete = datafile.sql_query_from_array(query)
    assert sql_delete == "DELETE FROM elements WHERE record_id = 1"
    result = datafile.sql_query(sql_delete)
    assert result

    # bad delete, missing where clause
    with pytest.raises(sqlite3.Error) as exc_info:
        query = {"type": "delete", "table": "elements"}
        sql = datafile.sql_query_from_array(query)
        result = datafile.sql_query(sql)
    exc_raised = exc_info.value
    assert exc_info.typename == "OperationalError"
    datafile_close(datafile)


def test_02_17_sql_query_from_array_update(tmp_path):
    filename, datafile = base_setup(tmp_path)
    value_set = {
        "record_id": None,
        "installed": False,
        "remarks": "another iffy remark",
    }
    query = {"type": "insert", "table": "elements"}
    sql = datafile.sql_query_from_array(query, value_set)
    result = datafile.sql_query(sql, value_set)
    assert result

    index = datafile.sql_nextid(result)
    value_set["installed"] = True
    query = {"type": "update", "table": "elements"}
    query["where"] = "record_id = " + str(index)
    sql = datafile.sql_query_from_array(query, value_set)
    result = datafile.sql_query(sql, value_set)
    assert result
    datafile_close(datafile)


def test_02_18_sql_query_from_array_select(tmp_path):
    filename, datafile = base_setup(tmp_path)
    value_set = {
        "record_id": None,
        "installed": False,
        "remarks": "another iffy remark",
    }
    query_insert = {"type": "insert", "table": "elements"}
    sql = datafile.sql_query_from_array(query_insert, value_set)
    result = datafile.sql_query(sql, value_set)

    query_select = {"type": "select", "table": "elements", "columns": "*"}
    sql = datafile.sql_query_from_array(query_select)
    result = datafile.sql_query(sql, value_set)
    assert result
    new_row = datafile.sql_fetchrow(result)
    assert new_row["record_id"] == 1
    assert new_row["remarks"] == value_set["remarks"]
    assert new_row["installed"] == value_set["installed"]
    query_select = {"type": "select", "table": "elements", "keys": "[*]"}
    sql = datafile.sql_query_from_array(query_select)
    result = datafile.sql_query(sql, value_set)
    assert result
    new_rows = datafile.sql_fetchrowset(result)
    assert len(new_rows) == 1

    query_select = {
        "type": "select",
        "table": "elements",
        "columns": ["record_id", "remarks", "installed"],
    }
    sql = datafile.sql_query_from_array(query_select)
    result = datafile.sql_query(sql)
    assert result

    new_row = datafile.sql_fetchrow(result)
    assert new_row["record_id"] == 1
    assert new_row["remarks"] == value_set["remarks"]
    assert new_row["installed"] == value_set["installed"]
    assert len(new_row) == 3

    sql = datafile.sql_query_from_array(query_insert, value_set)
    result = datafile.sql_query(sql, value_set)
    assert result
    sql = datafile.sql_query_from_array(query_select, value_set)
    result = datafile.sql_query(sql, value_set)
    assert result
    new_rows = datafile.sql_fetchrowset(result)
    assert len(new_rows) == 2

    query_select = {
        "type": "select",
        "table": "elements",
        "columns": ["record_id", "remarks", "installed"],
        "order_by": "record_id DESC",
    }
    sql = datafile.sql_query_from_array(query_select)
    result = datafile.sql_query(sql, value_set)
    assert result
    new_rows = datafile.sql_fetchrowset(result)
    assert len(new_rows) == 2
    assert new_rows[1]["record_id"] < new_rows[0]["record_id"]

    query_select = {
        "type": "select",
        "table": "elements",
        "columns": ["record_id", "remarks", "installed"],
        "limit": ["1"],
    }
    sql = datafile.sql_query_from_array(query_select)
    result = datafile.sql_query(sql, value_set)
    assert result
    new_rows = datafile.sql_fetchrowset(result)
    assert len(new_rows) == 1
    assert new_rows[0]["record_id"] == 1

    query_select = {
        "type": "select",
        "table": "elements",
        "columns": ["record_id", "remarks", "installed"],
        "limit": ["1", "1"],
    }
    sql = datafile.sql_query_from_array(query_select)
    result = datafile.sql_query(sql, value_set)
    assert result
    new_rows = datafile.sql_fetchrowset(result)
    assert len(new_rows) == 1
    assert new_rows[0]["record_id"] == 2

    query_select = {"type": "select", "table": "elements", "where": "record_id = 2"}
    sql = datafile.sql_query_from_array(query_select)
    result = datafile.sql_query(sql)
    assert result
    new_row = datafile.sql_fetchrow(result)
    assert new_row["record_id"] == 2
    datafile_close(datafile)


def test_02_19_new_db_file(tmpdir):
    # create a new database with the given name and table structure.
    path = tmpdir.mkdir("new_database").join("test.db")
    DataFile.new_file(path, datafile_definition)
    assert os.path.exists(path)

    # test that the new database file is correct.
    datafile = DataFile()
    datafile.sql_connect(path)
    assert datafile.sql_is_connected()

    query = "SELECT name FROM  sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%'"
    result = datafile.sql_query(query)
    table_names = datafile.sql_fetchrowset(result)
    assert len(table_names) == 1
    assert table_names[0]["name"] == "elements"

    query = "PRAGMA table_info('elements');"
    result = datafile.sql_query(query)
    column_names = datafile.sql_fetchrowset(result)
    print(column_names)
    expected_names = ["record_id", "remarks", "installed"]
    for col in column_names:
        assert col["name"] in expected_names
    datafile_close(datafile)
