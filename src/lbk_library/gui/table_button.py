"""
A QPushButton to be placed in a TablePushButtonGroup in a QTableWidget cell.

File:       table_push_button.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file LICENSE
"""

from PyQt5.QtWidgets import QPushButton, QTableWidget


class TablePushButton(QPushButton):
    """
    Extend QPushButton redirecting a clicked signal to cellClicked signal.

    The cellClicked signal will hold the current row and button_id values.
    """

    def __init__(self, table: QTableWidget, row: int, button_id: int) -> None:
        """
        Setup the TablePushButton.

        The button default state is set to False. The button redirects
        the "clicked" signal to the Table signal 'cellClicked' signal
        with the row and button_id as the parameters.

        Parameters:
            table (QTableWdiget): the table to place this button group.
            row (int): the row for the button group:
            button_id (int): the identifing number of the button
        """
        super().__init__()

        self.table = table
        self.row = row
        self.button_id = button_id

        self.setDefault(False)
        self.setAutoDefault(False)
        self.clicked.connect(self.button_clicked)

    def button_clicked(self) -> None:
        """
        Redirect the button's "clicked" signal to the table's
        "cell clicked" signal.

        The redirected signal is emitted with the cell row and the
        button_id as parameters. The "clicked" parameter of the
        "clicked" signal is discarded.
        """
        self.table.cellClicked.emit(self.row, self.button_id)
