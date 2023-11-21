"""
An error indicating combo box widget to be placed in a QTableWidget cell.

File:       table_combo_boxt.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file LICENSE
"""

from PyQt5.QtCore import pyqtProperty
from PyQt5.QtWidgets import QFrame, QTableWidget, QWidget

from .combo_box import ComboBox
from .error_frame import ErrorFrame


class TableComboBox(QWidget):
    """
    An error indicating ComboBox widget for QTableWidget use.

    This will place a CmboBox widget inside an ErrorFramewidget with
    necessary functionality to cleanly operate as part of a QTableWidget
    cell.
    """

    def __init__(
        self, table: QTableWidget, row: int, column: int, selection_list: [str]
    ):
        """
        Initialize the TableComboBox.

        The comboBox widget is initialized with the given row and
        column, and white border. The 'combo box 'activated' signal is
        redirected to the Table 'cellChanged' signal with the row,
        column and current text as the parameters.

        Parameters:
            table (QTableWidget): the table to place this ComboBox.
            row (int) the cell row for the widget.
            column (int) the cell column where the widget will be placed.
        """
        super().__init__()
        self.table = table
        self._row = row
        self._column = column

        self.error_frame = ErrorFrame(self)
        self.error_frame.setFrameShape(QFrame.NoFrame)
        self.combo_box = ComboBox(self.error_frame)
        self.combo_box.clear()
        self.combo_box.addItems(selection_list)
        self.combo_box.setCurrentIndex(-1)
        self.combo_box.setFrame(False)

        self.combo_box.activated.connect(self.activated)

    def activated(self):
        """
        Redirect 'activated' signal to 'cellChanged' signal.

        The redirected signal is emitted with the cell row and column
        as parameters.
        """
        self.table.cellChanged.emit(self._row, self._column)

    def setCurrentText(self, text: str) -> None:
        """
        Set the text property of the ComboBox.

        Parameters:
            text (str): the text to place in the ComboBox box.
        """
        self.combo_box.setCurrentText(text)

    def currentText(self) -> int:
        """
        Get the currentText property of the ComboBox.

        Returns:
            (int) The current text in the ComboBox.
        """
        return self.combo_box.currentText()

    def setCurrentIndex(self, index: int) -> None:
        """
        Set the current index property of the ComboBox.

        Parameters:
            index (int): the index to set in the ComboBox.
        """
        self.combo_box.setCurrentIndex(index)

    def currentIndex(self) -> str:
        """
        Get the currentIndex property of the ComboBox.

        Returns:
            (int) The current index in the ComboBox.
        """
        return self.combo_box.currentIndex()

    def resizeEvent(self, event):
        """
        Size the TableComboBox to the size of the cell.

        The ErrorFrame component is set to the size of the cell. The
        ComboBox component is centered within the ErrorFrame with a
        2 pixel margin on all sides to allow the ErrorFrame border
        to show.

        Parameters:
            event (ResizeEvent): event triggered whenever the cell is
                resized.
        """
        self.error_frame.setGeometry(0, 0, event.size().width(), event.size().height())
        self.combo_box.setGeometry(
            2, 2, event.size().width() - 4, event.size().height() - 4
        )

    @pyqtProperty(int)
    def row(self) -> int:
        """Get the table row."""
        return self._row

    @row.setter
    def row(self, value: int) -> None:
        """Set the table row."""
        self._row = value

    @pyqtProperty(int)
    def column(self) -> int:
        """Get the table column."""
        return self._column

    @column.setter
    def column(self, value: int) -> None:
        """Set the table column."""
        self._column = value
