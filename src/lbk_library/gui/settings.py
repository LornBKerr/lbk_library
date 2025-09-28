"""
Extend QtCore.QSettings to make retrieving a List from settings easier.

File:       settings.py
Author:     Lorn B Kerr
Copyright:  (c) 2025 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    1.1.0
"""

from typing import Any

from PySide6.QtCore import QSettings

file_name = "settings.py"
file_version = "1.1.0"
changes = {"1.0.0": "Initial release", "1.1.0": "Added get and set boolean values."}


class Settings(QSettings):
    """
    This adds functionality to QSettings to do some common tasks.

    read_list() and write_list(): The ability to read and write lists
    with a one-line call is provided.

    set_bool_value() and bool_value(): Boolean values can be read and
    written ensuring that the values are either True or False
    automatically string and numeric variants of true and false.

    Dictionaries can be converted to QSettings object and QSettings objects
    can be converted to dictionaries.

    All other aspects of QSettings are unchanged.
    """

    def write_list(self, prefix: str, values: list[Any], size: int = -1):
        """
        Write a python list to a QSettings array.

        Parameters:
            prefix (str): The QSettings key to hold the list.
            size (int): the length of the list; defaults to -1 (to be
                automatically determined).
        """
        self.beginWriteArray(prefix)
        for i in range(len(values)):
            self.setArrayIndex(i)
            self.setValue("entry", values[i])
        self.endArray()
        self.sync()  # ensure the settings object is updated now

    def read_list(self, prefix: str, size: int = -1) -> list[str]:
        """
        Read a python list from a QSettings array.

        Parameters:
            prefix (str): The QSettings key to hold the list.
            size (int): the length of the list; defaults to -1; defaults
                to -1 to be automatically determined).
        """
        new_list = []
        size = self.beginReadArray(prefix)
        for i in range(size):
            self.setArrayIndex(i)
            new_list.append(self.value("entry", i))
        self.endArray()

        return new_list

    def set_bool_value(self, key: str, value: Any) -> bool:
        """
        Set a boolean value in the config settings.

        Parameters:
            value (Any): a boolean type value; one of '1' (string), 1 (int),
                True (boolean), 'True' or 'true' are the only allowed
                values to return True. All other values ar considered
                False. (This is more restrictive than standard python.)
            key (str): The config key for this value.
        """
        result = False
        if value in (True, "1", 1, True, "True", "true"):
            result = True
        self.setValue(key, result)
        return result

    def bool_value(self, key: str) -> bool:
        """
        Get a boolean value in the config settings.

        Parameters:
            key (str): The config key for this value.
        """
        result = self.value(key)
        if self.value(key) is None:
            result = False
        return bool(result)
