"""
A group of TablePushButtons.

This will contain one or more TablePushButtons evenly spaced horizontally in
the Table cell.

File:       table_button_group.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file LICENSE
"""

from PyQt5.QtWidgets import QFrame, QHBoxLayout, QPushButton, QTableWidget

from .table_push_button import TablePushButton


class TableButtonGroup(QFrame):
    """
    A group of TablePushButtons.

    This will contain one or more TablePushButtons evenly spaced
    horizontally in the Table cell.
    """

    def __init__(self, table: QTableWidget, row: int, column: int) -> None:
        """
        Initialize a button group for placement in the Table Widget.

        Parameters:
            table (QTableWdiget): the table to place this button group.
            row (int): the row for the button group.
            column (int): the column for the button group.
        """
        super().__init__()
        self.table: QTableWidget = table
        self.row: int = row
        self.column: int = column
        self.buttons: dict[int, TablePushButton] = {}

        # set up QHBoxLayout
        self.frame_layout = QHBoxLayout(self)
        self.frame_layout.setContentsMargins(1, 1, 1, 1)
        self.frame_layout.setSpacing(3)

        # set up QFrame
        self.setContentsMargins(1, 1, 1, 1)
        self.setLayout(self.frame_layout)

    def add_button(self, text: str, button_id: int) -> QPushButton:
        """
        Add a TablePushButton to the Button Group.

        Parameters:
            text (string) the text label for the button.
            button_id (int) the id number for this button.

        Returns:
            (QPushButton) the newly created button.
        """
        button = TablePushButton(self.table, self.row, button_id)
        button.setText(text)
        self.buttons[button_id] = button
        self.frame_layout.addWidget(button)
        return button
