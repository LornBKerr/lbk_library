"""
Implement a DataFile for permanent storage of information.

File:       datafile.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2024 Lorn B Kerr
License:    MIT, see file License
Version:    1.1.0
"""

import sqlite3
from traceback import print_exc
from typing import Any

file_version = "1.1.0"
changes = {
    "1.0.0": "Initial release",
    "1.1.0": "Changed name from 'Dbal' to 'DataFile'.",
}


class DataFile:
    """
    Implement a DataFile for permanent storage of information.

    This supplies the required minimum functionality to use the Sqlite3
    datafile.

    This is inspired by and modeled on the DataFile of PHPBB3, much
    simplified and implemented in python.
    """

    @classmethod
    def new_file(cls, filename: str, sql_statements: list[str]) -> None:
        """
        Create and initialize the new DataFile.

        Parameters:
            filename (str): full path to the datafile file to be created.
            sql_statements (list[str]): the sql definition of the
                datafile as a list of one or more SQL commands.
        """
        datafile = DataFile()
        datafile.sql_connect(filename)
        for sql in sql_statements:
            datafile.sql_query(sql)
        return datafile

    def __init__(self) -> None:
        """Create a new DataFile object."""
        self.__datafile_name: str = ""
        """Full path to the datafile in use."""
        self.__connection: sqlite3.Connection = None
        """Sqlite3 datafile connection object."""

    def sql_connect(self, datafile: str) -> bool:
        """
        Connect to a specific datafile.

        The variable __connection holds the connection object.

        Parameters:
            datafile (str): path to datafile from program root
                directory.

        Returns:
            (bool) True if connection succeeded, false otherwise
        """
        self.datafile_name = datafile
        return_value = False
        try:
            self.__connection = sqlite3.connect(self.datafile_name)
            # set the row to be a dictionary (map or associative array)
            self.__connection.row_factory = self.__dict_factory
            return_value = True
        except sqlite3.Error:
            self._sql_error("Database Connection Error")

        if return_value:
            # Set the encoding for new datafiles,
            # ignored by existing datafiles.
            self.sql_query('PRAGMA encoding = "UTF-8"', [])
        return return_value

    def sql_query(self, query: str, values: dict = {}) -> sqlite3.Cursor:
        """
        Execute a sql datafile query.

        Parameters:
            query (str): Contains the SQL query statement which shall be
                executed.
            values (dict): The name: values pairs to inserted into the
                query; not all statements require this; default is
                empty dict.

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

    def _sql_error(self, sql_text: str = "") -> None:
        """
        Display the error.

        Parameters:
            sql_text (str): the sql command in error
        """
        print(sql_text)
        print_exc()

    def sql_close(self) -> None:
        """Close sql connection."""
        if self.__connection:
            self.__connection.close()
            self.__connection = None

    def sql_is_connected(self) -> bool:
        """
        Check the status of the datafile connection.

        Returns:
            (bool) True if connected, False if not
        """
        return bool(self.__connection)

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

    def sql_nextid(self, query_result: sqlite3.Cursor) -> int:
        """
        Get last inserted id after an insert statement.

        This is only valid after Insert queries.

        Parameters:
            query_result (sqlite3.Cursor): The result of a previous
                query operation.

        Returns:
            (int) the last id assigned if the last query was valid,
                otherwise 0.
        """
        nextid = 0
        if query_result:
            nextid = query_result.lastrowid
        return nextid

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

    def sql_fetchrowset(self, query_result: sqlite3.Cursor) -> list:
        """
        Fetch all rows from a query result.

        Parameters:
            query_result (Sqlite3.Cursor): The result of the previous
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

    def sql_query_from_array(self, query: dict, value_set: dict = {}) -> str:
        """
        Build parameterized sql statement from array.

        Only DELETE, INSERT, UPDATE and SELECT statements are handled.

        Parameters:
            query (dict): {
                ['type'] -> (str) one of 'DELETE', 'INSERT', 'SELECT',
                            or 'UPDATE'
                ['table'] -> (str) name of table to access
                ['where'] -> (str) providing the sql where_clause
                    contents (without the 'WHERE").Required for DELETE
                    statements, Optional for SELECT statements, not used
                    by other statements.
                ['columns'] -> (list) column names for INSERT and SELECT
                    statements. SELECT statement may use just [*] to
                    select all columns. If ommitted, defaults to '*'.
                ['values'] -> (list) The set of values to insert or
                    update. Order must match ['keys']
                ['order_by'] -> (str) providing the sql 'order by'
                    clause (without the "ORDER_BY"). Optional for the
                    SELECT statement, not used by other statments
                ['limit'] -> list: [0] =int(limit value)
                                   [1] = int(offset value)
                    Optional for SELECT statements, not used by
                    other statements
                }
            value_set (dict): holds the key => value pairs for all the
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
                sql = ""  # Bad type, not one of DELETE, INSERT, SELECT, or UPDATE
        return sql

    def __sql_delete_statement(self, query: dict) -> str:
        """
        Build the sql DELETE statement.

        Statement Form:  DELETE FROM table WHERE x = y

        Parameter:
            query (dict): {
                ['type'] -> (str) 'DELETE',
                ['table'] -> (str) name of table to access
                ['where'] -> (str) the sql where_clause contents
                    (without the 'WHERE').

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

    def __sql_insert_statement(self, query: dict, value_set: dict[str, Any]) -> str:
        """
        Build the sql INSERT query statement.

        Statement Form: INSERT INTO table (column1, column2,...columnN)
            VALUES (value1, value2,...valueN)

        Parameters:
            query (dict): {
                ['type'] -> (str) 'INSERT'
                ['table'] -> (str) name of table
                value_set -> (dict) set of key->value pairs to insert
                    into table
            }

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

    def __sql_select_statement(self, query: dict) -> str:
        """
        Build the sql SELECT query statement.

        Statement form: SELECT 'column1', 'column2',...  'columnN'
                    FROM 'table_name'
                    WHERE x = y
                    ORDER BY 'columnX'
                    LIMIT 5 OFFSET 0

        Parameters:
            query (dict): {
                ['type'] -> (str) 'SELECT'
                ['table'] -> (str) name of table
                ['columns'] -> (list) column names for SELECT statement.
                    Statement may use just '[*]' or '*' to select all
                    columns. If omitted, defaults to '*'.
                ['where'] -> (str) providing the sql where_clause
                    contents (without the 'WHERE"). Optional, if not
                    present, selects all rows.
                ['order_by'] -> (str) providing the sql 'order by'
                    clause (without the "ORDER_BY"). Optional
                ['limit'] -> (list)
                    [0] = (int) limit value,
                    [1] = (int) offset value. Optional
            }

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

    def __sql_update_statement(self, query: dict, value_set: dict) -> str:
        """
        Build the sql UPDATE query statement.

        Statement Form:
            UPDATE table_name
            SET column1 = value1, column2 = value2...., columnN = valueN
            WHERE [condition];

        Paraeters:
            query (dict): {
                ['type']  -> (str) 'UPDATE'
                ['table'] -> (str) name of table
                ['where'] -> (str) providing the sql where_clause
                    contents selecting a specific row
            }
            value_set (dict): holding the set of values to update

        Return;
            (str) resultant sql query statement
        """
        sql = "UPDATE " + query["table"] + " SET "
        # set clause
        set_list = []
        for key in value_set.keys():
            if key != "record_id":
                set_list.append(key + " = " + ":" + key)
        sql += ", ".join(set_list)
        # where clause
        if query["where"]:
            sql += " WHERE " + query["where"]
        return sql

    def __dict_factory(self, cursor: sqlite3.Cursor, row: list[Any]) -> dict:
        """Set the return from a fetchrow function to be a dict object."""
        dict_row: dict[str, Any] = {}
        for idx, col in enumerate(cursor.description):
            dict_row[col[0]] = row[idx]
        return dict_row
