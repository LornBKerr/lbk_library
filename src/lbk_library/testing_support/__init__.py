"""
The Project Library Collection.

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

File:       __init__.py
Author:     Lorn B Kerr
Copyright:  (c) 2024 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    1.0.1
"""

from .core_setup import (
    datafile_close,
    datafile_create,
    datafile_open,
    directories,
    filesystem,
    load_datafile_table,
    long_string,
    test_string,
)

file_version = "1.0.1"
changes = {
    "1.0.0": "Initial release",
    "1.0.1": "Added version info.",
}
