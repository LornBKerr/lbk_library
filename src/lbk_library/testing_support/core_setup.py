"""
Test setup for general test functionality.

This module provides a number of values and functions to help setup the
general test environment for different projects. All test modules draw
on a varying selection of these values.

Values Available:
    test_string - A string for testing where a string is needed.
    long_string - A string exceeding the base 255 character upper limit.

Filesystem, Directories and associated files:
    directories (list): List of directories for the filesystem.
    filesystem(tmp_path): Pytest fixture to generate a temporary
        filesystem.
Data File Handling:
    datafile_open(: Function to open a database in temporary file system
        returning a reference to the database.
    datafile_create: Function to create a new database returning a
        reference to the new database.
    datafile_close: function to close the open datafile.
    load_datafile_table: Function to load a specific datafile table.
    load_all_datafile_tables(test_file) : Function to load all datafile
        tables.

File:       core_setup.py
Author:     Lorn B Kerr
Copyright:  (c) 2024 Lorn B Kerr
License:    MIT, see file License
"""

import pytest

from lbk_library import DataFile

# Directories for Windows and Linux
directories = [
    ".config",
    "Documents",
    "Documents/parts_tracker",
]

# some test strings
test_string = "This is a string"

long_string = ""
while len(long_string) < 255:
    long_string = long_string + ", " + test_string


@pytest.fixture
def filesystem(tmp_path):
    """
    Setup a temporary filesystem which will be discarded after the test
    sequence is run.

    'base_dir' is the directory structure for saving and retrieving data
    with two directories: '.config' and 'Documents'. This directory
    structure will be discarded after the test sequence is run.

    Parameters:
        tmp_path: pytest fixture to setup a path to a temperary location

    Returns:
        (str) The temporary test base directory..
    """
    base_dir = tmp_path / "base_dir"
    base_dir.mkdir()

    # make a set of base_dir directories and files
    for directory in directories:
        a_dir = base_dir / directory
        a_dir.mkdir()

    return str(base_dir)


def datafile_open(filepath: str):
    """
    Open a DataFile.

    Parameters:
        filepath (str): full path to a data_file.

    Returns:
        (DataFile) reference to the opened test_file.
    """
    test_file = DataFile()
    test_file.sql_connect(filepath)
    return test_file


def datafile_close(test_file: DataFile):
    """
    Close an open database.

    Parameters:
        test_file (DataFile): The open datafile to be closed.
    """
    test_file.sql_close()


def datafile_create(filepath: str, datafile_definition: str):
    """
    Create a new, empty test_file.

    Parameters:
        filepath (DataFile): The full path to the requested test_file.

    Returns:
         (DataFile) reference to the opened test_file.
    """
    test_file = datafile_open(filepath)
    for sql in datafile_definition:
        test_file.sql_query(sql)
    return test_file


def load_datafile_table(test_file, table_name, column_names, value_set):
    """Load one of the database tables with a set of values."""
    sql_query = {"type": "INSERT", "table": table_name}
    for values in value_set:
        entries = {}
        i = 0
        while i < len(column_names):
            entries[column_names[i]] = values[i]
            i += 1
        sql = test_file.sql_query_from_array(sql_query, entries)
        test_file.sql_query(sql, entries)
