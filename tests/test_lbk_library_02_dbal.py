# command --> pytest --cov-report term-missing --cov=lbk_library tests/

""" Test file for lbk_library Dbal Object"""

import os
import sqlite3
import sys

import pytest

if "/home/larry/development/lbk_library/src" not in sys.path:
    sys.path.append("/home/larry/development/lbk_library/src")

from lbk_library import Dbal

database = "./test.db"


def close_database(dbref):
    dbref.sql_close()


def delete_database():
    os.remove(database)


@pytest.fixture
def dbal_open_database():
    dbref = Dbal()
    # valid connection
    dbref.sql_connect(database)
    return dbref


@pytest.fixture
def open_create_table():
    dbref = Dbal()
    dbref.sql_connect(database)
    dbref.sql_query("DROP TABLE IF EXISTS 'test_table'")
    create_table = (
        'CREATE TABLE IF NOT EXISTS "test_table"'
        + '("record_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,'
        + ' "remarks" TEXT DEFAULT NULL,'
        + ' "installed" BOOLEAN)'
    )
    dbref.sql_query(create_table)
    return dbref


def test_01_dbal_constructor():
    dbref = Dbal()
    assert isinstance(dbref, Dbal)


def test_02_sql_connect_invalid():
    dbref = Dbal()
    # invalid connection because of invalid path
    connection = dbref.sql_connect("./database/nn.db")
    assert not connection
    close_database(dbref)


def test_03_sql_connect_valid(dbal_open_database):
    dbref = dbal_open_database
    assert dbref.sql_is_connected()
    close_database(dbref)


def test_04_sql_close(dbal_open_database):
    dbref = dbal_open_database
    assert dbref.sql_is_connected()
    dbref.sql_close()
    assert not dbref.sql_is_connected()
    close_database(dbref)


def test_05_sql_bad_statement(dbal_open_database):
    dbref = dbal_open_database
    with pytest.raises(sqlite3.Error) as exc_info:
        sql = "SELECT * FROM"  # missing table name
        result = dbref.sql_query(sql)
    exc_raised = exc_info.value
    assert exc_info.typename == "OperationalError"
    close_database(dbref)


def test_06_sql_validate_value_none(dbal_open_database):
    dbref = dbal_open_database
    result = dbref.sql_validate_value(None)
    assert result is None
    close_database(dbref)


def test_07_sql_validate_value_bool(dbal_open_database):
    dbref = dbal_open_database
    result = dbref.sql_validate_value(True)
    assert isinstance(result, int)
    assert result == 1
    result = dbref.sql_validate_value(False)
    assert isinstance(result, int)
    assert result == 0
    close_database(dbref)


def test_08_sql_validate_value_string(dbal_open_database):
    dbref = dbal_open_database
    result = dbref.sql_validate_value("a string")
    assert isinstance(result, str)
    assert result == "'a string'"
    close_database(dbref)


def test_09_sql_nextid_none(dbal_open_database):
    dbref = dbal_open_database
    result = dbref.sql_nextid(None)
    assert result == 0
    close_database(dbref)


def test_10_sql_validate(dbal_open_database):
    dbref = dbal_open_database
    assert dbref.sql_validate_value(None) == None
    assert dbref.sql_validate_value("test") == "'test'"
    assert dbref.sql_validate_value(10) == 10
    assert dbref.sql_validate_value(True) == 1
    assert dbref.sql_validate_value(False) == 0
    close_database(dbref)


def test_11_sql_fetchrow_none(dbal_open_database):
    dbref = dbal_open_database
    result = dbref.sql_fetchrow(None)
    assert not result
    close_database(dbref)


def test_12_sql_fetchrowset_none(dbal_open_database):
    dbref = dbal_open_database
    result = dbref.sql_fetchrowset(None)
    assert len(result) == 0
    close_database(dbref)


def test_13_sql_query_from_array_none(open_create_table):
    # No data should return empty string
    dbref = open_create_table
    assert dbref
    result = dbref.sql_query_from_array(None)
    assert result == ""
    close_database(dbref)


def test_14_sql_query_from_array_bad_query(open_create_table):
    # query not a dict should return false
    dbref = open_create_table
    query = list()
    result = dbref.sql_query_from_array(query)
    assert not result
    close_database(dbref)


def test_15_sql_query_from_array_bad_type(open_create_table):
    dbref = open_create_table
    query = {"type": "GiveMe"}
    assert not dbref.sql_query_from_array(query)
    close_database(dbref)


def test_16_sql_query_from_array_delete(open_create_table):
    dbref = open_create_table
    value_set = {"installed": False, "remarks": "another iffy remark"}
    query = {"type": "insert", "table": "test_table"}
    sql_insert = dbref.sql_query_from_array(query, value_set)
    assert (
        sql_insert
        == "INSERT INTO test_table (installed, remarks) VALUES (:installed, :remarks)"
    )
    result = dbref.sql_query(sql_insert, value_set)
    assert isinstance(result, sqlite3.Cursor)
    index = dbref.sql_nextid(result)
    assert index == 1

    # good delete
    query = {"type": "delete", "table": "test_table"}
    query["where"] = "record_id = " + str(index)
    sql_delete = dbref.sql_query_from_array(query)
    assert sql_delete == "DELETE FROM test_table WHERE record_id = 1"
    result = dbref.sql_query(sql_delete)
    assert result

    # bad delete, missing where clause
    with pytest.raises(sqlite3.Error) as exc_info:
        query = {"type": "delete", "table": "test_table"}
        sql = dbref.sql_query_from_array(query)
        result = dbref.sql_query(sql)
    exc_raised = exc_info.value
    assert exc_info.typename == "OperationalError"
    close_database(dbref)


def test_17_sql_query_from_array_update(open_create_table):
    dbref = open_create_table
    value_set = {"installed": False, "remarks": "another iffy remark"}
    query = {"type": "insert", "table": "test_table"}
    sql = dbref.sql_query_from_array(query, value_set)
    result = dbref.sql_query(sql, value_set)
    assert result

    index = dbref.sql_nextid(result)
    value_set["installed"] = True
    query = {"type": "update", "table": "test_table"}
    query["where"] = "record_id = " + str(index)
    sql = dbref.sql_query_from_array(query, value_set)
    result = dbref.sql_query(sql, value_set)
    assert result
    close_database(dbref)


def test_18_sql_query_from_array_select(open_create_table):
    dbref = open_create_table
    value_set = {"installed": False, "remarks": "another iffy remark"}
    query_insert = {"type": "insert", "table": "test_table"}
    sql = dbref.sql_query_from_array(query_insert, value_set)
    result = dbref.sql_query(sql, value_set)

    query_select = {"type": "select", "table": "test_table", "columns": "*"}
    sql = dbref.sql_query_from_array(query_select)
    result = dbref.sql_query(sql, value_set)
    assert result
    new_row = dbref.sql_fetchrow(result)
    assert new_row["record_id"] == 1
    assert new_row["remarks"] == value_set["remarks"]
    assert new_row["installed"] == value_set["installed"]
    query_select = {"type": "select", "table": "test_table", "keys": "[*]"}
    sql = dbref.sql_query_from_array(query_select)
    result = dbref.sql_query(sql, value_set)
    assert result
    new_rows = dbref.sql_fetchrowset(result)
    assert len(new_rows) == 1

    query_select = {
        "type": "select",
        "table": "test_table",
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
        "table": "test_table",
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
        "table": "test_table",
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
        "table": "test_table",
        "columns": ["record_id", "remarks", "installed"],
        "limit": ["1", "1"],
    }
    sql = dbref.sql_query_from_array(query_select)
    result = dbref.sql_query(sql, value_set)
    assert result
    new_rows = dbref.sql_fetchrowset(result)
    assert len(new_rows) == 1
    assert new_rows[0]["record_id"] == 2

    query_select = {"type": "select", "table": "test_table", "where": "record_id = 2"}
    sql = dbref.sql_query_from_array(query_select)
    result = dbref.sql_query(sql)
    assert result
    new_row = dbref.sql_fetchrow(result)
    assert new_row["record_id"] == 2
    close_database(dbref)


def test_19_cleanup(dbal_open_database):
    dbref = dbal_open_database
    result = dbref.sql_query("DROP TABLE IF EXISTS 'test_table'")
    assert result
    close_database(dbref)
    delete_database()


# end lbk_library_02_dbal.py
