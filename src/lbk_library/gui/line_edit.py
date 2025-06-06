"""
Extend QLineEdit handling the focus lost event.

File:       line_edit.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    1.1.0
"""

from PySide6.QtCore import Property
from PySide6.QtGui import QFocusEvent
from PySide6.QtWidgets import QLineEdit, QWidget

from .error_frame import ErrorFrame

file_version = "1.1.0"
changes = {
    "1.0.0": "Initial release",
    "1.1.0": "Changed library 'PyQt5' to 'PySide6'",
}


class LineEdit(QLineEdit):
    """Converts a 'focus out' event to 'editingFinshed' signal."""

    def __init__(self, parent: QWidget = None) -> None:
        """
        Extend the QLineEdit converting the QFocusEvent

        Parameters:
            parent(QWidget) the parent widget holding the QLineEdit,
                default is None.
        """
        super().__init__(parent)

        self.error_frame = None
        self._error = False

    def set_error_frame(self, frame: ErrorFrame = None) -> None:
        """Set the related ErrorFrame."""
        self.error_frame = frame

    def focusOutEvent(self, evt: QFocusEvent) -> None:
        """
        Emit the line edit 'editingFinished' signal when focus is lost.

        Parameters:
            evt (QFocusEvent): event triggered whe the focus is lost
        """
        self.editingFinished.emit()
        super().focusOutEvent(evt)

    @Property(bool)
    def error(self) -> bool:
        """Get the error status."""
        return self._error

    @error.setter
    def error(self, value: bool) -> None:
        """Set the error status."""
        self._error = value
        self.error_frame.error = value
