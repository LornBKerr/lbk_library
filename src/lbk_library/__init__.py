"""
The Project Library Collection.

This contains common classes that support several projects.

This module contains the following classes
    Dbal            A database abstraction layer for SQLite3
    Element         Base class for types of information in a database
    ElementSet      Base class for a set of basic elements
    IniFileParser   Read and Write *.ini Files
    Validate        Support validation of values going into the database

File:       lbk_library/__init__.py
Version:    0.3.1
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    see License.txt
"""

import configparser
import datetime
import os
import re
import sqlite3
import sys
from collections.abc import Iterator
from copy import deepcopy
from traceback import print_exc
from typing import Any, Union


def __init__() -> None:
    """Initialize the lbk_library module."""


# end __init()


class Dbal:
    """
    Database Abstraction Layer Implementation.

    This supplies the required minimum functionality to use the Sqlite3
    database.

    This is inspired by and modeled on the Dbal of PHPBB3, much
    simplified and implemented in python.
    """

    def __init__(self) -> None:
        """Create a new Dbal object."""
        self.__dbname: str = ""
        """ full path to the database in use """
        self.__connection: sqlite3.Connection = None
        """ sqlite3 database connection object """

    # end __init()

    def sql_connect(self, database: str) -> bool:
        """
        Connect to a specific Sqlite3 database.

        The class variable __connection holds the connection object.

        Parameters:
            database: (str) path to database from program root
                directory.

        Returns:
            (bool) True if connection succeeded, false otherwise
        """
        #        Raises:  <-  Not true
        #            sqlite3.Error if the connection fails
        self.__dbname = database
        """ full path to database file"""
        return_value = False
        try:
            self.__connection = sqlite3.connect(
                self.__dbname,
                5.0,
                sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            )
            # set the row to be a dictionary (map or associative array)
            self.__connection.row_factory = self.__dict_factory
            return_value = True
        except sqlite3.Error:
            self._sql_error("Database Connection Error")

        if return_value:
            # Set the encoding for new databases,
            # ignored for existing databases.
            self.sql_query('PRAGMA encoding = "UTF-8"', [])
        return return_value

    # end sql_connect()

    def sql_query(self, query: str, values: dict = {}) -> sqlite3.Cursor:
        """
        Execute a sql database query.

        Parameters:
            query: (str) Contains the SQL query statement which shall be
                executed.
            values: (dict) The name: values to inserted into the query;
                not all statements require this; default is empty dict.

        Returns:
            (sqlite3.Cursor) the query result status if query succeeded,
                 None Otherwise
        Raises:
            sqlite3.OperationalError: if query is not valid
        """
        query_result = None
        try:
            if self.__connection:
                query_result = self.__connection.cursor()
                query_result.execute(query, values)
                self.__connection.commit()
        except sqlite3.OperationalError:
            query_result = None  # sqlite3.Cursor()
            self._sql_error(query)
            raise sqlite3.OperationalError
        return query_result

    # end sql_query()

    def _sql_error(self, sql_text: str = "") -> None:
        """
        Display the error.

        Parameters:
            sql_text: (str) the sql command in error
        """
        print(sql_text)
        print_exc()

    # end _sql_error()

    def sql_close(self) -> None:
        """Close sql connection."""
        if self.__connection:
            self.__connection.close()
            self.__connection = None

    # end sql_close()

    def sql_is_connected(self) -> bool:
        """
        Check the status of the database connection.

        Returns:
            (bool) True if connected, False if not
        """
        return bool(self.__connection)

    # end is_connected()

    def sql_validate_value(self, var: Any) -> Any:
        """
        Validate values for inclusion in SQL statements.

        Returns:
            (Any) Updated values for None, Strings, and Booleans,
                otherwise the unchanged variable value.
        """
        return_value: Any = None
        if var is None:
            return_value = None
        elif isinstance(var, str):
            return_value = "'" + var + "'"
        elif isinstance(var, bool):
            if var:
                return_value = 1
            else:
                return_value = 0
        else:
            return_value = var
        return return_value

    # end sql_validate_value()

    def sql_nextid(self, query_result: sqlite3.Cursor) -> int:
        """
        Get last inserted id after an insert statement.

        This is only valid after Insert queries.

        Parameters:
            query_result: (sqlite3.Cursor) The result of a previous
                query operation.

        Returns:
            (int) the last id assigned if the last query was valid,
                otherwise 0.
        """
        nextid = 0
        if query_result:
            nextid = query_result.lastrowid
        return nextid

    # end sql_nextid()

    def sql_fetchrow(self, query_result: sqlite3.Cursor) -> dict:
        """
        Fetch current row from the query result set.

        Parameters:
            query_result (Sqlite3.Cursor) The result of the previous
                query operation.

        Returns:
            (dict) the current row as a dict(), None if no more rows or
                invalid query_result
        """
        row = {}
        if query_result:
            row = query_result.fetchone()
        return row

    # end sql_fetchrow()

    def sql_fetchrowset(self, query_result: sqlite3.Cursor) -> list:
        """
        Fetch all rows from a query result.

        Parameters:
            query_result (Sqlite3.Cursor) The result of the previous
                query operation.

        Returns:
            (list) The full set of rows as a list of dict objects,
                empty list if an invalid query result or when no rows
                are available.
        """
        rows = []
        if query_result:
            rows = query_result.fetchall()
        return rows

    # end sql_fetchrowset()

    def sql_query_from_array(self, query: dict, value_set: dict = {}) -> str:
        """
        Build parameterized sql statement from array.

        Only DELETE, INSERT, UPDATE and SELECT statements are handled.

        Parameters:
            query: (dict) {
                ['type'] -> (str) one of 'DELETE', 'INSERT', 'SELECT',
                            or 'UPDATE'
                ['table'] -> (str) name of table to access
                ['where'] -> (str) providing the sql where_clause
                            contents (without the 'WHERE").Required
                            for DELETE statements, Optional for SELECT
                            statements, not used by other statements.
                ['columns'] -> (list) column names for INSERT and SELECT
                            statements. SELECT statement may use just [*]
                            to select all columns. If ommitted, defaults
                            to '*'.
                ['values'] -> (list) The set of values to insert or
                            update. Order must match ['keys']
                ['order_by'] -> (str) providing the sql 'order by' clause
                            (without the "ORDER_BY"). Optional for the
                            SELECT statement, not used by other statments
                ['limit'] -> list: [0] =int(limit value)
                                   [1] = int(offset value)
                            Optional for SELECT statements, not used by
                            other statements
                }
            value_set: (dict) holds the key => value pairs for all the
                parameters needed in building the sql statement.

        Returns:
            (str) The results of building the statement. An empty string
                will be returned if the query is not a dictionary or the
                type is not one of DELETE, INSERT, UPDATE or SELECT.
        """
        if not isinstance(query, dict):
            sql = ""
        else:
            sql = query["type"].upper()
            if sql == "DELETE":
                sql = self.__sql_delete_statement(query)
            elif sql == "INSERT":
                sql = self.__sql_insert_statement(query, value_set)
            elif sql == "SELECT":
                sql = self.__sql_select_statement(query)
            elif sql == "UPDATE":
                sql = self.__sql_update_statement(query, value_set)
            else:
                sql = ""  # Bad type, not one of DELETE, INSERT,
                #  SELECT, or UPDATE
        return sql

    # end sql_query_from_array()

    def __sql_delete_statement(self, query: dict) -> str:
        """
        Build the sql DELETE statement.

        Statement Form:  DELETE FROM table WHERE x = y

        Parameter:
            query (dict)<br/>&emsp;&emsp;['type'] - (str) 'DELETE'
            <br/>&emsp;&emsp;['table'] - (str) name of table to access
            <br/>&emsp;&emsp;['where'] - (str) the sql where_clause
                contents (without the 'WHERE').

        Returns:
            (str) the fully formed DELETE statement.
        """
        sql = query["type"].upper() + " FROM " + query["table"]
        try:
            if query["where"]:
                sql += " WHERE " + query["where"]
        except KeyError:
            sql += " WHERE "  # illegal where clause
        return sql

    # end __sql_delete_statement()

    def __sql_insert_statement(self, query: dict, value_set: dict[str, Any]) -> str:
        """
        Build the sql INSERT query statement.

        Statement Form: INSERT INTO table (column1, column2,...columnN)
            VALUES (value1, value2,...valueN)

        Parameters:
            query: (dict)<br/>&emsp;&emsp;['type'] - (str) 'INSERT'
                <br/>&emsp;&emsp;['table'] - (str) name of table
            value_set: (dict) set of key->value pairs to insert into
                table

        Returns:
            (str) INSERT sql statement.
        """
        sql = query["type"].upper() + " INTO " + query["table"] + " "
        keys = value_set.keys()
        columns = "(" + ", ".join(keys) + ")"
        holder = []
        for key in keys:
            holder.append(":" + key)
        placeholder = "(" + ", ".join(holder) + ")"
        sql += columns + " VALUES " + placeholder
        return sql

    # end __sql_insert_statement()

    def __sql_select_statement(self, query: dict) -> str:
        """
        Build the sql SELECT query statement.

        Statement form: SELECT 'column1', 'column2',...  'columnN'
                    FROM 'table_name'
                    WHERE x = y
                    ORDER BY 'columnX'
                    LIMIT 5 OFFSET 0

        Parameters:
            query: (dict) {
                <br/>&emsp;&emsp;['type'] -> (str) 'SELECT'
                <br/>&emsp;&emsp;['table'] -> (str) name of table
                <br/>&emsp;&emsp;['columns'] -> (list) column names for
                    SELECT statement. Statement may use just '[*]' or
                    '*' to select all columns. If omitted, defaults to
                    '*'.
                <br/>&emsp;&emsp;['where'] -> (str) providing the sql
                    where_clause contents (without the 'WHERE").
                    Optional, if not present, selects all rows.]
                <br/>&emsp;&emsp;['order_by'] -> string providing the
                    sql 'order by' clause (without the "ORDER_BY").
                    Optional
                <br/>&emsp;&emsp;['limit'] -> (list)
                    [0] = (int)limit value,
                    [1] = (int)offset value. Optional
                <br/>&emsp;&emsp;}

        Returns:
            (str) resultant sql query statement
        """
        sql = "SELECT"
        try:  # columns to select
            if query["columns"] == "*" or query["columns"][0] == "*":
                sql += " * "
            else:
                sql += " " + ", ".join(query["columns"])
        except KeyError:
            sql += " * "
        sql += " FROM " + query["table"] + " "
        try:
            if query["where"]:
                sql += " WHERE " + query["where"]
        except KeyError:
            pass
        try:
            if query["order_by"]:
                sql += " ORDER BY " + query["order_by"]
        except KeyError:
            pass
        try:
            if query["limit"]:
                sql += " LIMIT " + query["limit"][0]
                if query["limit"][1]:
                    sql += " OFFSET " + query["limit"][1]
        except KeyError:
            pass
        except IndexError:
            pass

        return sql

    # end __sql_select_statement()

    def __sql_update_statement(self, query: dict, value_set: dict) -> str:
        """
        Build the sql UPDATE query statement.

        Statement Form:
            UPDATE table_name
            SET column1 = value1, column2 = value2...., columnN = valueN
            WHERE [condition];

        Paraeters:
            query: (dict) {
                <br/>&emsp;&emsp;['type']  -> (str) 'UPDATE'
                <br/>&emsp;&emsp;['table'] -> (str) name of table
                <br/>&emsp;&emsp;['where'] -> (str) providing the sql
                    here_clause contents selecting a specific row
                }
            value_set: (dict) holding the set of values to update

        Return;
            (str) resultant sql query statement
        """
        sql = "UPDATE " + query["table"] + " SET "
        # set clause
        set_list = []
        for key in value_set.keys():
            if key != "entry_index":
                set_list.append(key + " = " + ":" + key)
        sql += ", ".join(set_list)
        # where clause
        if query["where"]:
            sql += " WHERE " + query["where"]
        return sql

    # end __sql_update_statement()

    def __dict_factory(self, cursor: sqlite3.Cursor, row: list[Any]) -> dict:
        """Set the return from a fetchrow function to be a dict object."""
        dict_row: dict[str, Any] = {}
        for idx, col in enumerate(cursor.description):
            dict_row[col[0]] = row[idx]
        return dict_row

    # end __dict_factory()


# end class Dbal


class Element:
    """
    This is the base class for types of information in the database.

    Element contains methods to get, add, delete and update information
    in the database. The set_properties() method must be overridden by
    the child classes for the specific type of element being implemented.
    """

    def __init__(
        self, dbref: Dbal, table_name: str, default_values: dict[str, Any] = None
    ) -> None:
        """
        Initialize a new Element object.

        Parameters:
            dbref: (Dbal) reference to the database holding the element
            table_name: (str) database table to search for the element
                values.
            default_values: (dict[str, Any]) the set of default values
                for this element, default is None. If not given,
                built-in defaults of {'entry_index': 0, 'remarks': ''}
                will be used.
        """
        self._validate: Validate = Validate()
        """ reference to the Validate class for value validation """

        self._defaults: dict[str, Any] = {"entry_index": 0, "remarks": ""}
        """ Default values for the Element """
        self.__dbref: Dbal = dbref
        """ The database instance to use """
        self.__table: str = table_name
        """ The database table for this instance """
        self.__properties: dict[str, Any] = {}
        """ The current values of this instance """
        self.__initial_values: dict[str, Any] = {}
        """ Hold the initial settings of the properties """
        self.__changed_properties: dict[str, bool] = {}
        """ boolean flags of properties changed, updated as entries are
            checked. Flag is set to True if value is changed, False if
            not """
        self.__properties_valid: dict[str, bool] = {}
        """(dict) set of boolean flags of element properties validated,
            each flag is set to False if value is invalid, True if
            value is valid """

        if default_values:  # set the current default values
            self._defaults = default_values
        self.set_initial_values(deepcopy(self._defaults))

    # end __init__()

    def get_properties_from_db(
        self, column_name: str, column_value: Any
    ) -> dict[str, Any]:
        """
        Retrieve the properties of a single element from the database.

        The requested element is selected by the table column name and
        the key column value designated.

        Parameters:
            column_name: (str) within the table containing the key values
            column_value: (Any) Key value requested

        Returns:
            (dict) Row containing requested element if successful or
            an empty dict object if not.
        """
        self.__properties = {}
        if column_name and column_value:
            query = {}
            query["type"] = "SELECT"
            query["table"] = self.__table
            query["keys"] = ["*"]
            query["where"] = (
                column_name + " = " + str(self.__dbref.sql_validate_value(column_value))
            )
            query_sql = self.__dbref.sql_query_from_array(query, {})
            query_result = self.__dbref.sql_query(query_sql, [])

            # get the row, if row not found, returns None
            self.__properties = self.__dbref.sql_fetchrow(query_result)
            if self.__properties is None:
                self.__properties = {}
        return self.__properties

    # end get_properties_from_db()

    def add(self) -> int:
        """
        Add an element to the database.

        Returns:
            (int) unique id of the newly added element or False if
                add failed
        """
        return_value = False
        property_set = self.get_properties()
        del property_set["entry_index"]  # new entry id will be assigned
        query = {
            "type": "insert",
            "table": self.get_table(),
        }
        sql = self.get_dbref().sql_query_from_array(query, property_set)
        result = self.get_dbref().sql_query(sql, property_set)
        if result:
            return_value = self.__dbref.sql_nextid(result)
            property_set["entry_index"] = return_value

        return return_value

    # end add_element()

    def delete(self) -> bool:
        """
        Delete an element from the database.

        This always uses the entry_index column and value to identify
        the record to delete.

        Returns:
            (bool) True if the deletion was successful, False if not.
        """
        return_value = False
        query = {
            "type": "delete",
            "table": self.get_table(),
            "where": "entry_index =" + str(self.get_entry_index()),
        }
        sql = self.__dbref.sql_query_from_array(query, [])
        result = self.get_dbref().sql_query(sql, [])
        if result:
            return_value = True
        return return_value

    # end delete_element()

    def update(self) -> bool:
        """
        Update an element in the database.

        This always uses the entry_index column and value to identify
        the record to update.

        Returns:
            (bool) True if the update was successful, False if not.
        """
        return_value = False
        # get the values to set, assume all but 'entry_index'
        property_set = self.get_properties()
        # query the database
        query = {"type": "update", "table": self.get_table()}
        query["where"] = "entry_index = " + str(property_set["entry_index"])
        sql = self.get_dbref().sql_query_from_array(query, property_set)
        result = self.get_dbref().sql_query(sql, property_set)
        if result:
            return_value = True

        return return_value

    # end update()

    def get_properties(self) -> dict[str, Any]:
        """
        Get the element properties as a dict() of property_names->values.

        Return (dict) The element properties.
        """
        return self.__properties

    # end get_properties()

    def set_properties(self, properties: dict[str, Any]) -> None:
        """
        Set the values of the Element properties array.

        This must be overridden and called by the child class to handle
        the full set of properties. This method sets the common
        properties 'entry_index' (contained in all Elements) and
        'remarks' (contained in many Elements).

        Each property is validated for type and value within an
        acceptable range, with unacceptable values set to the
        respective default values. Properties not part of the element
        are discarded.

        Parameters:
            properties: (dict) object holding the element values. Keys
            must match the required keys of the element being modified,
            properties may be sparse.
        """
        if properties is not None and isinstance(properties, dict):
            for key in properties.keys():
                if key == "entry_index":
                    self.set_entry_index(properties[key])
                elif key == "remarks":
                    self.set_remarks(properties[key])

    # end set_properties()

    def _get_property(self, name: str) -> Any:
        """
        Get an individual property value by Name.

        Parameters:
            name: (str) name of property to retrieve

        Returns:
            (Any) value of property if property is defined.

        Raises:
            KeyError: if name is not a valid property name.
        """
        return self.__properties[name]

    # end _get_property()

    def _set_property(self, name: str, value: Any) -> None:
        """
        Set an individual property.

        This is a low level function with no error checking.

        Parameters:
            name: (str) property name
            value: (Any) value of this property
        """
        self.__properties[name] = value

    # end _set_property()

    def get_entry_index(self) -> int:
        """
        Get the Elements's entry_index.

        Returns:
            (int) The Elements's entry_index or 0 if no entry_index is
                assigned
        """
        entry_index = self._get_property("entry_index")
        if entry_index is None:
            entry_index = self._defaults["entry_index"]
        return entry_index

    # end get_entry_index()

    def set_entry_index(self, entry_index: int) -> dict[str, Any]:
        """
        Set the Element's entry index.

        Parameters:
            entry_index: (int)  the new entry_index for the Element.
                Must be an integer greater than 0 and must be unique
                when Element is stored to the database (not checked).
                If the supplied entry_index is not valid, the
                entry_index is set to __defaults['entry_index'].

        Returns:
            (dict)<br>&emsp;&emsp;['entry'] - (int) the updated
                entry_index
            <br>&emsp;&emsp;['valid'] - (bool) True if the operation
                suceeded, False otherwise
            <br>&emsp;&emsp;['msg'] - (str) Error message if not valid
        """
        result = self._validate.integer_field(entry_index, self._validate.REQUIRED, 1)
        if result["valid"]:
            self._set_property("entry_index", result["entry"])
        else:
            self._set_property("entry_index", self._defaults["entry_index"])
        self.update_property_flags("entry_index", result["entry"], result["valid"])
        return result

    # end set_entry_index()

    def get_remarks(self) -> str:
        """
        Get the remarks for this Element.

        Returns:
            (str) The remarks for this Element, the default value if no
            remarks are assigned.
        """
        remarks = self._get_property("remarks")
        if remarks is None:
            remarks = self._defaults["remarks"]
        return remarks

    # end get_remarks()

    def set_remarks(self, remarks: str) -> dict[str, Any]:
        """
        Set the remarks for this Item.

        The remarks are optional and may be empty.

        Parameters:
            remarks: (str) For this Element, may be empty.

        Returns:
        (dict)<br>&emsp;&emsp;['entry'] - the updated remarks for this
            Element
            <br>&emsp;&emsp;['valid'] - (bool) True if the operation
                suceeded, False otherwise
            <br>&emsp;&emsp;['msg'] - (str) Error message if not valid
        """
        if remarks is None:
            remarks = ""
        result = self._validate.text_field(remarks, self._validate.OPTIONAL, 0)
        if result["valid"]:
            self._set_property("remarks", result["entry"])
        else:  # really no way to be here
            self._set_property("remarks", "")
        self.update_property_flags("remarks", result["entry"], result["valid"])
        return result

    # end set_remarks()

    def get_dbref(self) -> Dbal:
        """
        Get the database reference for this element.

        Returns:
            (Dbal) A reference to the current database
        """
        return self.__dbref

    # end get_dbref()

    def get_table(self) -> str:
        """
        Get the name of the database table for the child.

        Returns:
        (str) The table name for this element.
        """
        return self.__table

    # end get_table()

    def get_initial_values(self) -> dict[str, Any]:
        """
        Get the intial values for the element.

        Returns:
            (dict) the initial values assigned to the element's
            properties.
        """
        return self.__initial_values

    # end get_initial_values()

    def set_initial_values(self, initial_value_set: dict[str, Any]) -> None:
        """
        Set the initial settings for the element entries.

        The initial values are set. The changed flags are initialized
        to false. If the entry_index is an integer greater than 0, the
        valid flags are initialized to True, otherwise, False.

        Parameters:
            initial_value_set (dict) holds the intial values assigned to
            the element's properties.

        Raises:
            TypeError if 'initial_value_set' is not a dict
        """
        if isinstance(initial_value_set, dict):
            self.__initial_values = deepcopy(initial_value_set)
        else:
            raise TypeError(
                "Initial_value set must be a dict with the initial"
                + " values for the element"
            )

    # end set_initial_values()

    def update_property_flags(self, name: str, value: Any, valid: bool) -> None:
        """
        Update the flags for a property member.

        This updates the change flag and the valid flag for the named
        property member.

        Parameters:
            name: (str) the name of the specific property member
            value: (Any) the new property value
            valid: (bool) True if new value is valid, false if not
        """
        self.set_value_changed_flag(name, value)
        self.set_value_valid_flag(name, valid)

    # end update_property_flags()

    def get_value_changed_flag(self, entry_name: str) -> bool:
        """
        Get an value changed flag for the given property.

        The flag will be True if the property has changed from the
        initial value, False if not.

        Parameters:
            entry_name: (str) name of entry to check

        Returns:
            (bool) The state of the entry changed flag

        Raises:
            KeyError if entry_name is not a valid name
        """
        return self.__changed_properties[entry_name]

    # end get_value_changed_flag()

    def set_value_changed_flag(self, entry_name: str, entry_value: Any) -> bool:
        """
        Set an value changed flag.

        The given value changed flag is set True if the entry value has
        changed from the initial value, False if not.

        Parameters:
            entry_name (str) name of entry that changed
            entry_value: (Any) value of the entry that changed

        Returns:
            (bool) The updated state of the entry changed flag
        """
        self.__changed_properties[entry_name] = (
            self.__initial_values[entry_name] != entry_value
        )
        return self.__changed_properties[entry_name]

    # end set_value_changed_flag()

    def have_values_changed(self) -> bool:
        """
        Check the entry changed flags.

        The result is True if any value changed flag is set, False
        otherwise.

        Returns:
            (bool) True if any entry has changed, False if no entry
                has changed.
        """
        entries_changed = False
        for key in self.__changed_properties:
            if self.__changed_properties[key]:
                entries_changed = True
                break
        return entries_changed

    # end have_values_changed()

    def clear_value_changed_flags(self) -> None:
        """Clear the set of 'value changed' flags."""
        self.__changed_properties.clear()

    # end clear_value_changed_flags()

    def get_value_valid_flag(self, entry_name: str) -> bool:
        """
        Get a value valid flag.

        Parameteres:
            entry_name (str) entry to get validation flag

        Returns:
            (bool) the resulting flag value

        Raises:
            KeyError if entry_name is not in the value valid flag set
        """
        return self.__properties_valid[entry_name]

    # end get_value_valid_flag()

    def set_value_valid_flag(self, entry_name: str, entry_valid: bool) -> bool:
        """
        Set a entry valid flag.

        Parameters:
            entry_name: (str) entry to set validation flag
            entry_valid: (bool) True if entry is valid, False if not

        Returns:
            (bool) the resulting flag value
        """
        self.__properties_valid[entry_name] = entry_valid
        return self.__properties_valid[entry_name]

    # end set_value_valid_flag()

    def is_element_valid(self) -> bool:
        """
        Check the Element validity.

        Implicit here is that all properties have been checked for
        validity. This should be done as part of the element
        construction.

        Returns:
            (bool) True if all element values are valid, False otherwise.

        Raises:
            KeyError if entry_name is not a valid name
        """
        element_valid = True
        if not self.get_properties():
            # Can't be valid if no properties are defined
            element_valid = False
        for key in self.get_properties():
            element_valid = element_valid and self.get_value_valid_flag(key)
        return element_valid

    # end validate_dialog_entries()

    def clear_value_valid_flags(self) -> None:
        """Clear the set of 'valid' flags."""
        self.__properties_valid.clear()

    # end clear_value_valid_flags()


# end Class Element


class ElementSet:
    """
    The base class for a set of Elements in the database.

    The set of Element types must be all the same type. The class
    implements the "Iterator" interface.
    """

    def __init__(
        self,
        dbref: Dbal,
        table_name: str,
        element_type: type,
        where_column: str = None,
        where_value: Any = None,
        order_by_column: str = None,
        limit: int = None,
        offset: int = None,
    ) -> None:
        """
        Get a list of elements from the database table.

        This will return a list of rows from the database table where
        the 'where_column' contains the 'where_value'. The list can
        optionally be sorted ascending by the values in the
        'order_by_column'.

        The number of rows can be optionally limited to the number of
        rows in 'limit and the search will start at the row number
        (zero based) given in 'offset'.

        Parameters:
            dbref: (Dbal) reference to the database holding the element.
            table_name: (str) database table to search for the element
                values.
            element_type: (type) the type of element in the set,
            where_column: (str) The key column of the table containing
                the key value to determine the elements being retrieved.
                If null, all rows are retrieved.
            where_value: (Any) The key value to retrieve. Required if
                where_column is set.
            order_by_column: (str) one or more column names separated
                by commas to order the resulting set of elements.
            limit: (int) number of rows to retrieve, defaults to all.
            offset: (int) row number to start retrieval, 0 based,
                defaults to row 0.
        """
        self.__dbref: Dbal = dbref
        """ The database holding the element set """
        self.__table: str = table_name
        """ The database table for this element set """
        self.__property_set: list[Element] = []
        """ The set of elements in this element set """
        self.__position: int = -1
        """ The current iterator position in the property_set, """

        # set the initial query array
        query: dict[str, Any] = {"type": "SELECT", "table": self.__table}

        # case 1 - basic case: get all elements from table
        values: dict[str, Any] = {}
        query["where"] = ""

        # case 2 - selection case: get all elements from table matching column
        #          name and value
        if where_column is not None and where_value is not None:
            query["where"] = where_column + " = :" + where_column
            values[where_column] = where_value

            # case 3 - ordered result: results of case 1 or case 2
            #   ordered by one or more column name(s)
        if order_by_column is not None:
            query["order_by"] = order_by_column

            # case 4 - partial set: results of cases 1, 2 or 3 limited
            #   to a partial result
        if limit:
            query["limit"] = list(str(limit))
            values["limit"] = limit
            if offset:
                query["limit"].append(str(offset))
                values["offset"] = offset

        query_str = self.__dbref.sql_query_from_array(query, values)
        query_result = self.__dbref.sql_query(query_str, values)

        # get the rows, if rows not found, returns empty list
        self.__property_set = self.__dbref.sql_fetchrowset(query_result)

        # convert to a list of 'element_type'
        element_set = list()
        property_set = self.get_property_set()

        for row in property_set:
            element = element_type(self.get_dbref(), row)
            element.set_initial_values(row)
            element.set_properties(row)
            element_set.append(element)
        self.set_property_set(element_set)

    # end __init__()

    def append(self, element: Element) -> None:
        """
        Append an element to the end of the property set.

        Parameters:
            element: (Element) the element to append to the property set
        """
        self.insert(len(self.get_property_set()), element)

    # end append()

    def insert(self, index: int, element: Element) -> None:
        """
        Insert an element into the property set at a specific index.

        Parameters:
            index: (int) location to insert the element (zero based)
            element: (Element) the element to insert into the
                property set
        """
        self.get_property_set().insert(index, element)

    # end insert()

    def get(self, location: int) -> Element:
        """
        Get an element from the property set at the given index.

        Parameters:
            location: (int) index of the element to be retrieved
                (zero based)
        """
        return self.get_property_set()[location]

    # end delete()

    def delete(self, location: int) -> None:
        """
        Delete an element from the property set at the given index.

        Parameters:
            location: (int) index of the element to be deleted
                (zero based)
        """
        del self.get_property_set()[location]

    # end delete()

    def get_dbref(self) -> Dbal:
        """
        Get the database reference.

        Returns:
            (Dbal) The database reference for this element set.
        """
        return self.__dbref

    # end get_dbref()

    def get_table(self) -> str:
        """
        Get the database table name.

        Returns:
            (str) The table name for this element set.
        """
        return self.__table

    # end get_table()

    def set_table(self, table: str) -> None:
        """
        Set the database table name.

        Parameters:
            table (str) The table name for this element set.
        """
        self.__table = table

    # end set_table()

    def get_property_set(self) -> list[Element]:
        """
        Get the property set for this element set.

        Returns:
            (list) The property set for this element set.
        """
        return self.__property_set

    # end get_property_set()

    def set_property_set(self, property_set: list[Element]) -> None:
        """
        Set the property set array for this element set.

        Parameters:
            property_set: (list) property set for this element set. The
            list may be empty
        """
        if isinstance(property_set, list):
            self.__property_set = property_set
        else:
            self.__property_set = []

    # end set_property_set()

    def get_number_elements(self) -> int:
        """
        Get the number of elements in the element set.

        Returns:
            (int) Number of elements in the element set.
        """
        return len(self.get_property_set())

    # end get_number_elements()

    def build_option_list(self, key: str) -> list[str]:
        """
        Build a list from an element property set.

        This will be for properties such as entry_indices or names for
        use primarily in setting ComboBox selection lists.

        Parameters:
            key: (str) the element property to display in the
                option list

        Return:
            (list) List of element properties as strings
        """
        option_list = []
        for element in self.get_property_set():
            option_list.append(str(element.get_properties()[key]))
        return option_list

    # end build_option_list()

    # ***** Iterator Interface *****

    def __iter__(self) -> Iterator:
        """
        Generate an Iterator object for this element.

        Returns:
            (Iterator) This ElementSet reference as the Iterator Object.
        """
        return self

    # end __iter__()

    def __next__(self) -> Element:
        """
        Return the next Element in the set.

        Returns:
            (Element) next element in the set

        Raises:
            StopIteration When the last element of the set has been
            returned.
        """
        self.__position += 1
        if self.__position >= len(self.get_property_set()):
            self.__reset__()
            raise StopIteration  # signals "the end"
        return self.get_property_set()[self.__position]

    # end __next__()

    def __reset__(self) -> None:
        """Reset the iterator position to the beginning."""
        self.__position = -1

    # end __reset__()


# end class ElementSet


class Validate:
    """
    Provides various methods to validate variables.

    Validations are provided for Booleans, Dates, Floats, Integers, and
    Text fields.
    """

    REQUIRED = True
    """ (bool) variable is required and must satisfy the validation
    requirements """
    OPTIONAL = False
    """ (bool) variable is optional but, if present, must satisfy
    requirements. """

    def integer_field(
        self,
        value: Union[int, str],
        required: bool,
        min_value: int = 0,
        max_value: int = sys.maxsize,
    ) -> dict[str, Any]:
        """
        Validate a integer numeric field.

        The 'value' can be provided as a integer number or a string
        representation of an integer number.

        If the value is REQUIRED, the value must be present and a valid
        integer value or a string convertable to a integer. The empty
        string is not accepted as valid.

        If the value is OPTIONAL, the value must be present and be a
        valid integer value or a string convertable to a integer; the
        empty string ("") is accepted and converted  to int(0).

        Paramters:
            value: (int) number to be checked, an integer, a string
                representation of an integer, or "". The empty string is
                only accepted if the value is optional.
            required: (bool) one of the Validate.REQUIRED or
                Validate.OPTIONAL constants
            min_value: (int) minimum integer value, default is 0.
            max_value: (int) maximum integer value, default is the
                system maximum value for an int.

        Returns:
            (dict)<br>&emsp;&emsp;['entry'] - (int) validated version
                of input value.
            <br>&emsp;&emsp;['valid'] - (bool) True if the operation
                suceeded, False otherwise.
            <br>&emsp;&emsp;['msg']   - (str) Error message if not valid
        """
        result = {
            "entry": value,  # start with entered value
            "valid": True,  # assume success
            "msg": "",
        }  # with no error message

        if not isinstance(value, (int, str)):
            result["valid"] = False
            result["msg"] = (
                "Value must be a valid integer value or string"
                + " represention of a valid integer value"
            )

        if value == "":
            if required == self.OPTIONAL:
                value = 0
                result["entry"] = value
            else:
                result["valid"] = False
                result["msg"] = "An integer entry is required"

        if isinstance(value, str):
            # remove any leading or training white space
            value = value.strip()
            if re.match(r"^[-+]?([1-9]\d*|0)$", value):
                value = int(value)
                result["entry"] = value
            else:
                result["valid"] = False
                result["msg"] = "Value does not represent an Integer value"

        if result["valid"]:
            if value < min_value:
                result["valid"] = False
                result["msg"] = (
                    "The entry is less than the required"
                    + " minimum value of "
                    + str(min_value)
                )
            elif value > max_value:
                result["valid"] = False
                result["msg"] = (
                    "The entry is greater than the required"
                    + " maximum value of "
                    + str(max_value)
                )
        return result

    # end integer_field()

    def float_field(self, value, required, min_value=-1.0e8, max_value=1.0e8):
        """
        Validate a float numeric field.

        The 'value' can be provided as a float number or a string
        representation of a float number.

        If the value is REQUIRED, the value must be present and a valid
        float value or a string convertable to a float. The empty string
        is not accepted as valid.

        If the value is OPTIONAL, the value must be present and a valid
        float value or a string convertable to a float; the empty string
        ("") is accepted and converted to float(0).

        Parameters:
            value: (int) number to be checked, an integer, a string
                representationof an integer, or "". The empty string is
                only accepted if the value is optional.
        required: bool) one of the Validate.REQUIRED or
                Validate.OPTIONAL constants
        min_value: (float) the minimum acceptable value, default is
            float(-100,000,000.0)
        max_value: (float the maximum acceptable value, default is
            float(+100,000,000.0)

        Returns:
            (dict)<br>&emsp;&emsp;['entry']  - (float) validated version
                of input value.
            <br>&emsp;&emsp;['valid'] - (bool) True if the operation
                suceeded, False otherwise.
            <br>&emsp;&emsp;['msg'] - (str) Error message if not valid.
        """
        # initialize results array
        result = {
            "entry": value,  # start with entered value
            "valid": True,  # assume success
            "msg": "",
        }

        if not isinstance(value, (float, str)):
            result["valid"] = False
            result["msg"] = (
                "Value must be a valid float value or string"
                + " represention of a valid float value"
            )

        if value == "":
            if required == self.OPTIONAL:
                value = float(0)
                result["entry"] = value
            else:
                result["valid"] = False
                result["msg"] = "An float entry is required"

        if isinstance(value, str):
            # remove any leading or training white space
            value = value.strip()
            if re.match(r"^[+-]?\ *(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$", value):
                value = float(value)
                result["entry"] = value
            else:
                result["valid"] = False
                result["msg"] = "Value does not represent a Float value"

        if result["valid"]:
            if value < min_value:
                result["valid"] = False
                result["msg"] = (
                    "The entry is less than the required"
                    + " minimum value of "
                    + str(min_value)
                )
            elif value > max_value:
                result["valid"] = False
                result["msg"] = (
                    "The entry is greater than the required"
                    + " maximum value of"
                    + str(max_value)
                )
        return result

    # end float_field()

    def text_field(
        self, text: str, required: bool, min_length: int = 1, max_length: int = 255
    ) -> dict[str, Any]:
        """
        Validate a text field.

        The field needs a valid alphnumeric string, and optional minimum
        and maximum lengths of the field. Default values of 1 and 255
        are supplied for the minimum and maximum lengths. If the entry
        is marked as required, the entry must be present and match the
        length parameters. If not rquired (required = OPTIONAL), then
        the entry may be empty. If not empty, it must match the
        length parameters.

        The entered value should have all HTML tags including script
        tags and comments removed and all whitespace at the front and
        back of the string removed.

        Parameteres:
            text: (str) test to be checked.
        required: bool) one of the Validate.REQUIRED or
                Validate.OPTIONAL constants
        min_length: (int) minimum length in characters, optional,
            default is 1.
        max_length: (int) maximum length in characters, optional,
            default is 255.

        Returns:
            (dict)<br>&emsp;&emsp;['entry'] (int) cleaned version of
                input text.
            <br>&emsp;&emsp;['valid'] - (bool) True if the operation
                suceeded, False otherwise
            <br>&emsp;&emsp;['msg']   - (str) Error message if not valid
        """
        # initialize results array
        result = {
            "entry": text,  # start with empty text value
            "valid": True,  # assume success
            "msg": "",
        }  # with no error message

        if not isinstance(text, str):
            result["valid"] = False
            result["msg"] = "Value must be a valid string of text"

        if result["valid"] and required == self.REQUIRED and text == "":
            # required and empty
            result["valid"] = False
            result["msg"] = (
                "A text value ("
                + str(min_length)
                + " and "
                + str(max_length)
                + " characters long) is required and cannot be empty"
            )

            # check the length of the entry
        if result["valid"]:
            text = text.strip()  # remove leading and trailing whitespace
            if len(text) < min_length:
                result["valid"] = False
                result["msg"] = (
                    "The entered value is too short ( at least "
                    + str(min_length)
                    + " characters required)"
                )

            elif len(text) > max_length:
                result["valid"] = False
                result["msg"] = (
                    "The entered value is too long (no more than "
                    + str(max_length)
                    + " characters allowed"
                )
        return result

    # end text_field()

    def boolean(self, state: Any) -> dict[str, Any]:
        """
        Validate a boolean value.

        This will handle pure boolean values (True or False, 'true' or
        'false') or the value of an expression or widget widget that
        yields either 0 (false) or 1 (true), or the result of some
        operation that yields "on" or 'off".

        Parameters:
            state: (Any) of the boolean to be checked. A (bool) True,
                (str)g 'true', (str) '1', (int) 1, or (str) 'on' are
                accepted as True and (bool) False,  (str) 'false',
                (str) '0', (int) 0 or (str) 'off' are accepted as False.

        Returns:
            (dict)<br>&emsp;&emsp;['entry'] (bool) state converted to
                True or False
            <br>&emsp;&emsp;['valid'] - (bool) True if the operation
                 suceeded, False otherwise
            <br>&emsp;&emsp;['msg'] - (str) Error message if not valid
        """
        # initialize results array
        result = {
            "entry": 0,  # start with empty check box value
            "valid": True,  # assume success
            "msg": "",
        }  # with no error message

        if state in (True, "true", "on", "1", 1):
            result["entry"] = True
        elif state in (False, "false", "off", "0", 0):
            result["entry"] = False
        else:  # error in entry
            result["valid"] = False
            result["msg"] = "Invalid entry for boolean"

        return result

    # end boolean()

    def date_field(self, date_input: str, required: bool) -> dict[str, Any]:
        """
        Validate a date field.

        The field is a string representing a date. the representations
        accepted are:
        <br>&emsp;&emsp;mm/dd/yyyy such as '02/23/2015' or '2/3/2003'
        <br>&emsp;&emsp;yyyy-mm-dd such as '2015-23-03'
        <br>&emsp;&emsp;<strike>'Feb 23, 2015'</strike> (not Implemented)
        <br>&emsp;&emsp;<strike>'23 Feb, 2015'</strike> (not Implemented)

        The string input is converted to a date object and validated
        to be a valid date.

        Parameters:
            date_input: (str) date to be checked, may be an empty string
                if not REQUIRED
        required: bool) one of the Validate.REQUIRED or
                Validate.OPTIONAL constants

        Return:
            (dict)
            <br>&emsp;&emsp;['entry'] (str) the validated date if valid,
                 otherwise an empty string.
            <br>&emsp;&emsp;['valid'] - (bool) True if the operation
                suceeded, False otherwise.
            <br>&emsp;&emsp;['msg'] - (str) Error message if not valid.
        """
        # initialize results array
        result = {
            "entry": date_input,  # start with supplied value
            "valid": True,  # assume success
            "msg": "",
        }

        if not isinstance(date_input, str):  # string can be empty
            result["valid"] = False
            result["msg"] = "Value must be a valid string"
        else:
            date_input = date_input.strip()

        if result["valid"]:
            if date_input == "":
                if required == self.REQUIRED:  # required and empty
                    result["valid"] = False
                    result["msg"] = "A date value is required" " and cannot be empty"

        if result["valid"]:
            # build a datatime object to check things
            # mm/dd/yyyy; month and day either single or double digits
            if re.match(r"\d{1,2}/\d{1,2}/\d\d\d\d", date_input):
                date_array = date_input.split("/")
                try:
                    date_stamp = datetime.datetime(
                        int(date_array[2]), int(date_array[0]), int(date_array[1])
                    ).timestamp()
                except ValueError:
                    result["entry"] = date_input
                    result["valid"] = False
                    result["msg"] = (
                        date_input + " is not a valid date of form 02/23/2014"
                    )

                # yyyy-mm-dd    month and day either single or double digits
            elif re.match(r"\d\d\d\d-\d{1,2}-\d{1,2}", date_input):
                date_array = date_input.split("-")
                try:
                    date_stamp = datetime.datetime(
                        int(date_array[0]), int(date_array[1]), int(date_array[2])
                    ).timestamp()
                except ValueError:
                    result["entry"] = date_input
                    result["valid"] = False
                    result["msg"] = (
                        date_input + " is not a valid date of form 2015-23-03"
                    )

                # Bad entry
            else:
                result["entry"] = date_input
                result["valid"] = False
                result["msg"] = date_input + " is not recognizable as a valid date"
        return result

    # end date_field()


# end class Validate


class IniFileParser:
    """
    Exposes the stored configuation file (*.ini) as a standard dict.

    This uses the python 'configparser' object to provide 2 simple methods
    to read and write the full ini file. It initializes the config file
    directories and reads and writes ini files to and from the
    designated directories. For other needs, the full capabilities of
    the 'configparser' should be used.

    By default, it uses the standard Linux (Fedora) or Windows configuration
    locations.
    """

    def __init__(
        self, filename: str, program_config_subdir: str = "", config_dir: str = ""
    ) -> None:
        """
        Initialize the configuration file parser.

        This sets the configuration file location in the standard config
        directory, either '{HOME}/.config' for linux or '{HOME}/AppData'
        for Windows

        The resulting path to the config file is created if it does not
        already exist.

        Parameters:
            filename: (str) the config ini filename to be used.
            program_config_subdir: (str) (optional) the program specific
                sub-directory of the config directory location for this
                config file. Default is the empty string which
                defaults to filename minus the suffix.
            config_dir: (str) Used if the standard, platform dependent, config
                directory location is not desired for ssome reason (testing
                primarily)
        """
        home_dir = os.path.expanduser("~")

        self.config_file: str = ""
        """The full path to the ini file """

        # set the program config sub-dirirectory if not present
        if not program_config_subdir:
            program_config_subdir = os.path.splitext(filename)[0]

        # set the full path to the program config file directiory
        if not config_dir:
            if sys.platform.startswith("linux"):
                config_dir = os.path.join(home_dir, ".config", program_config_subdir)
            elif sys.platform.startswith("win"):
                config_dir = os.path.join(
                    home_dir, "AppData", "Roaming", program_config_subdir
                )
        else:
            config_dir = os.path.join(config_dir, program_config_subdir)

        # if no path to config file, create path
        if not os.path.exists(config_dir):
            print(config_dir)
            os.makedirs(config_dir, 0o744)

            # build the absolute file name.
        self.config_file = os.path.join(config_dir, filename)

    # end __init()

    def read_config(self) -> dict[str, Any]:
        """
        Read the configuration file.

        Everything is treated as a string, so any numbers or booleans
        will need to be converted separately.

        Returns:
            (dict) The saved configuration settings. If the config file
            does not exist, returns an empty dict object
        """
        config: dict[str, Any] = {}
        config_parser = configparser.ConfigParser(allow_no_value=True)

        # read the file
        if os.path.exists(self.config_file):
            config_parser.read_file(open(self.config_file, "r"))
            for section in config_parser.sections():
                config[section] = {}
                for key in config_parser[section]:
                    config[section][key] = config_parser[section].get(key)
        return config

    # end get_config()

    def write_config(self, new_config: dict[str, Any]) -> None:
        """
        Save the config values to the file.

        Parameters:
            new_config: (dict) The new configuration settings to save.
        """
        config_parser = configparser.ConfigParser(allow_no_value=True)
        config_parser.read_dict(new_config)
        config_parser.write(open(self.config_file, "w"))

    # end write_config()


# end class IniFileParser

# end module common.py
