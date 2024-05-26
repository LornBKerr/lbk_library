"""
Extends QTableWidgetItem to properly handle sorting of integer field items.

This overloads the 'less than' comparison function to properly handle
integers instead of strings.
"""

from PyQt5.QtWidgets import QTableWidgetItem


class TableWidgetIntItem(QTableWidgetItem):
    def __init__(self, integer_value: int) -> None:
        """
        Initalize a TableWidget item with an integer value.

        Parameters:
            integer_value (int) an integer to be stored in the table.
        """
        new_type = 1001
        """Set a unique type for the Table WidgetItem"""

        super().__init__(str(integer_value), new_type)

    def __lt__(self, other):
        """
        Provides the boolean less than test for integer table widget items.

        Returns:
            (Boolen) True if this item is less than the other item, False otherwise.
        """
        value = int(self.text())
        other_value = int(other.text())
        return value < other_value
