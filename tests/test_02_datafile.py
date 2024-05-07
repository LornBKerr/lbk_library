"""
Tests for the Dbal Class.

File:       test_02_dbal.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT, see file License
"""

""" Test file for lbk_library Dbal Object"""

import os
import sqlite3
import sys

import pytest

src_path = os.path.join(os.path.realpath("."), "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from test_setup import db_close, db_create, db_name, db_open, sql_statements

from lbk_library import Dbal


def test_02_01_dbal_constructor():
    dbref = Dbal()
    assert isinstance(dbref, Dbal)


def test_02_02_sql_connect_invalid():
    dbref = Dbal()
    # invalid connection because of invalid path
    connection = dbref.sql_connect("./database/nn.db")
    assert not connection


def test_02_03_sql_connect_valid(tmpdir):
    path = tmpdir / db_name
    dbref = Dbal()
    dbref.sql_connect(path)
    assert dbref.sql_is_connected()


def test_02_02_sql_close(db_open):
    dbref = db_open
    assert dbref.sql_is_connected()
    dbref.sql_close()
    assert not dbref.sql_is_connected()


def test_02_05_sql_bad_statement(db_open):
    dbref = db_open
    with pytest.raises(sqlite3.Error) as exc_info:
        sql = "SELECT * FROM"  # missing table name
        result = dbref.sql_query(sql)
    exc_raised = exc_info.value
    assert exc_info.typename == "OperationalError"
    db_close(dbref)


def test_02_06_sql_validate_value_none(db_open):
    dbref = db_open
    result = dbref.sql_validate_value(None)
    assert result is None
    db_close(dbref)


def test_02_07_sql_validate_value_bool(db_open):
    dbref = db_open
    result = dbref.sql_validate_value(True)
    assert isinstance(result, int)
    assert result == 1
    result = dbref.sql_validate_value(False)
    assert isinstance(result, int)
    assert result == 0
    db_close(dbref)


def test_02_08_sql_validate_value_string(db_open):
    dbref = db_open
    result = dbref.sql_validate_value("a string")
    assert isinstance(result, str)
    assert result == "'a string'"
    db_close(dbref)


def test_02_09_sql_nextid_none(db_open):
    dbref = db_open
    result = dbref.sql_nextid(None)
    assert result == 0
    db_close(dbref)


def test_02_10_sql_validate(db_open):
    dbref = db_open
    assert dbref.sql_validate_value(None) is None
    assert dbref.sql_validate_value("test") == "'test'"
    assert dbref.sql_validate_value(10) == 10
    assert dbref.sql_validate_value(True) == 1
    assert dbref.sql_validate_value(False) == 0
    db_close(dbref)


def test_02_11_sql_fetchrow_none(db_open):
    dbref = db_open
    result = dbref.sql_fetchrow(None)
    assert not result
    db_close(dbref)


def test_02_12_sql_fetchrowset_none(db_open):
    dbref = db_open
    result = dbref.sql_fetchrowset(None)
    assert len(result) == 0
    db_close(dbref)


def test_02_13_sql_query_from_array_none(db_create):
    # No data should return empty string
    dbref = db_create
    assert dbref
    result = dbref.sql_query_from_array(None)
    assert result == ""
    db_close(dbref)


def test_02_14_sql_query_from_array_bad_query(db_create):
    # query not a dict should return false
    dbref = db_create
    query = list()
    result = dbref.sql_query_from_array(query)
    assert not result
    db_close(dbref)


def test_02_15_sql_query_from_array_bad_type(db_create):
    dbref = db_create
    query = {"type": "GiveMe"}
    assert not dbref.sql_query_from_array(query)
    db_close(dbref)


def test_02_16_sql_query_from_array_delete(db_create):
    dbref = db_create
    value_set = {"installed": False, "remarks": "another iffy remark"}
    query = {"type": "insert", "table": "elements"}
    sql_insert = dbref.sql_query_from_array(query, value_set)
    assert (
        sql_insert
        == "INSERT INTO elements (installed, remarks) VALUES (:installed, :remarks)"
    )
    result = dbref.sql_query(sql_insert, value_set)
    assert isinstance(result, sqlite3.Cursor)
    index = dbref.sql_nextid(result)
    assert index == 1

    # good delete
    query = {"type": "delete", "table": "elements"}
    query["where"] = "record_id = " + str(index)
    sql_delete = dbref.sql_query_from_array(query)
    assert sql_delete == "DELETE FROM elements WHERE record_id = 1"
    result = dbref.sql_query(sql_delete)
    assert result

    # bad delete, missing where clause
    with pytest.raises(sqlite3.Error) as exc_info:
        query = {"type": "delete", "table": "elements"}
        sql = dbref.sql_query_from_array(query)
        result = dbref.sql_query(sql)
    exc_raised = exc_info.value
    assert exc_info.typename == "OperationalError"
    db_close(dbref)


def test_02_17_sql_query_from_array_update(db_create):
    dbref = db_create
    value_set = {"installed": False, "remarks": "another iffy remark"}
    query = {"type": "insert", "table": "elements"}
    sql = dbref.sql_query_from_array(query, value_set)
    result = dbref.sql_query(sql, value_set)
    assert result

    index = dbref.sql_nextid(result)
    value_set["installed"] = True
    query = {"type": "update", "table": "elements"}
    query["where"] = "record_id = " + str(index)
    sql = dbref.sql_query_from_array(query, value_set)
    result = dbref.sql_query(sql, value_set)
    assert result
    db_close(dbref)


def test_02_18_sql_query_from_array_select(db_create):
    dbref = db_create
    value_set = {"installed": False, "remarks": "another iffy remark"}
    query_insert = {"type": "insert", "table": "elements"}
    sql = dbref.sql_query_from_array(query_insert, value_set)
    result = dbref.sql_query(sql, value_set)

    query_select = {"type": "select", "table": "elements", "columns": "*"}
    sql = dbref.sql_query_from_array(query_select)
    result = dbref.sql_query(sql, value_set)
    assert result
    new_row = dbref.sql_fetchrow(result)
    assert new_row["record_id"] == 1
    assert new_row["remarks"] == value_set["remarks"]
    assert new_row["installed"] == value_set["installed"]
    query_select = {"type": "select", "table": "elements", "keys": "[*]"}
    sql = dbref.sql_query_from_array(query_select)
    result = dbref.sql_query(sql, value_set)
    assert result
    new_rows = dbref.sql_fetchrowset(result)
    assert len(new_rows) == 1

    query_select = {
        "type": "select",
        "table": "elements",
        "columns": ["record_id", "remarks", "installed"],
    }
    sql = dbref.sql_query_from_array(query_select)
    result = dbref.sql_query(sql)
    assert result

    new_row = dbref.sql_fetchrow(result)
    assert new_row["record_id"] == 1
    assert new_row["remarks"] == value_set["remarks"]
    assert new_row["installed"] == value_set["installed"]
    assert len(new_row) == 3

    sql = dbref.sql_query_from_array(query_insert, value_set)
    result = dbref.sql_query(sql, value_set)
    assert result
    sql = dbref.sql_query_from_array(query_select, value_set)
    result = dbref.sql_query(sql, value_set)
    assert result
    new_rows = dbref.sql_fetchrowset(result)
    assert len(new_rows) == 2

    query_select = {
        "type": "select",
        "table": "elements",
        "columns": ["record_id", "remarks", "installed"],
        "order_by": "record_id DESC",
    }
    sql = dbref.sql_query_from_array(query_select)
    result = dbref.sql_query(sql, value_set)
    assert result
    new_rows = dbref.sql_fetchrowset(result)
    assert len(new_rows) == 2
    assert new_rows[1]["record_id"] < new_rows[0]["record_id"]

    query_select = {
        "type": "select",
        "table": "elements",
        "columns": ["record_id", "remarks", "installed"],
        "limit": ["1"],
    }
    sql = dbref.sql_query_from_array(query_select)
    result = dbref.sql_query(sql, value_set)
    assert result
    new_rows = dbref.sql_fetchrowset(result)
    assert len(new_rows) == 1
    assert new_rows[0]["record_id"] == 1

    query_select = {
        "type": "select",
        "table": "elements",
        "columns": ["record_id", "remarks", "installed"],
        "limit": ["1", "1"],
    }
    sql = dbref.sql_query_from_array(query_select)
    result = dbref.sql_query(sql, value_set)
    assert result
    new_rows = dbref.sql_fetchrowset(result)
    assert len(new_rows) == 1
    assert new_rows[0]["record_id"] == 2

    query_select = {"type": "select", "table": "elements", "where": "record_id = 2"}
    sql = dbref.sql_query_from_array(query_select)
    result = dbref.sql_query(sql)
    assert result
    new_row = dbref.sql_fetchrow(result)
    assert new_row["record_id"] == 2
    db_close(dbref)


def test_02_19_new_db_file(tmpdir):
    # create a new database with the given name and table structure.
    path = tmpdir.mkdir("new_database").join("test.db")
    Dbal.new_file(path, sql_statements)
    assert os.path.exists(path)


#    dbref = Dbal()
#    dbref.sql_connect(path)
#    assert dbref.sql_is_connected()
#
#    query = "SELECT name FROM  sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%'"
#    result = dbref.sql_query(query)
#    table_names = dbref.sql_fetchrowset(result)
#    assert len(table_names) == 1
#    assert table_names[0]["name"] == "elements"
#
#    query = "PRAGMA table_info('elements');"
#    result = dbref.sql_query(query)
#    column_names = dbref.sql_fetchrowset(result)
#    print(column_names)
#    expected_names = ["record_id", "remarks", "installed"]
#    for col in column_names:
#        assert col["name"] in expected_names
