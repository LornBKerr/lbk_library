"""
An error indicating line edit widget to be placed in a QTableWidget cell.

File:       table_line_edit.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file LICENSE
"""

from PyQt5.QtCore import pyqtProperty
from PyQt5.QtWidgets import QTableWidget, QWidget

from .error_frame import ErrorFrame
from .line_edit import LineEdit


class TableLineEdit(QWidget):
    """
    An error indicating LineEdit widget for QTableWidget use.

    This will place a LineEdit widget inside an ErrorFramewidget with
    necessary functionality to cleanly operate as part of a QTableWidget
    cell.
    """

    def __init__(self, table: QTableWidget, row: int, column: int, alignment):
        """
        Initialize the TableLineEdit.

        The line edit widget is initialized with the given row and
        column, white border and the requested text alignment. The
        'LineEdit.editingFinished' signal is redirected to the Table
        signal 'cellChanged' signal with the row, column and text as
        the parameters.

        Parameters:
            table (QTableWidget): the table to place this LineEdit.
            row (int) the cell row for the widget.
            column (int) the cell column where the widget will be placed.
            alignment (int) some combination of Qt.Alignnment values.
        """
        super().__init__()
        self.table = table
        self._row = row
        self._column = column

        self.error_frame = ErrorFrame(self)
        self.line_edit = LineEdit(self.error_frame)
        self.line_edit.setFrame(False)

        self.line_edit.setAlignment(alignment)
        self.line_edit.editingFinished.connect(self.editing_finished)

    def editing_finished(self):
        """
        Redirect 'editingFinished' signal to 'cellChanged' signal.

        The redirected signal is emitted with the cell row and column
        as parameters.
        """
        self.table.cellChanged.emit(self._row, self._column)

    def set_text(self, text: str) -> None:
        """
        Set the text property of the LineEdit.

        Parameters:
            text (str): the text to place in the LineEdit box.
        """
        self.line_edit.setText(text)

    def text(self) -> str:
        """
        Get the text property of the LineEdit.

        Returns:
            (str) The text in the LineEdit box.
        """
        return self.line_edit.text()

    def set_read_only(self, read_only: bool) -> None:
        """
        Set the readOnly property of the QLineEdit.

        Parameters:
            read_only (bool): True if the line edit is to be read only,
                False if not.
        """
        self.line_edit.setReadOnly(read_only)

    def resizeEvent(self, event):
        """
        Size the TableLineEdit to the size of the cell.

        The ErrorFrame component is set to the size of the cell. The
        LineEdit component is centered within the ErrorFrame with a
        2 pixel margin to allow the ErrorFrame border to show.

        After the event is handled, it is passed to the super class.

        Parameters:
            event (ResizeEvent): event triggered whenever the cell is
                resized.
        """
        self.error_frame.setGeometry(0, 0, event.size().width(), event.size().height())
        self.line_edit.setGeometry(
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
