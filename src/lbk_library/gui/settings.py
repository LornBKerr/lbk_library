"""
Extend QtCore.QSettings to make retrieving a List from settings easier.

File:       settings.py
Author:     Lorn B Kerr
Copyright:  (c) 2025 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    1.0.0
"""

from typing import Any

from PySide6.QtCore import QSettings

file_name = "settings.py"
file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
}


class Settings(QSettings):
    """
    This adds functionality to set and retrieve Lists as one-line calls.

    All other aspects of QSettings are unchanged.
    """

    def write_list(self, values: list[Any], prefix: str, size: int = -1):
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
