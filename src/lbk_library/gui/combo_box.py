"""
Extend QComboBox to emit the activate signal when the focus is lost.

Error indication is added thru the use of ErrorFrame.

File:       combo_box.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    1.1.0
"""

file_version = "1.1.0"
changes = {
    "1.0.0": "Initial release",
    "1.1.0": "Changed library 'PyQt5' to 'PySide6'",
}

from PySide6.QtCore import Property
from PySide6.QtGui import QFocusEvent
from PySide6.QtWidgets import QComboBox, QFrame, QWidget

from .error_frame import ErrorFrame


class ComboBox(QComboBox):
    """Extend QComboBox to emit the activate signal if focus is lost."""

    def __init__(self, parent: QWidget = None) -> None:
        """
        Initialize the Combo Box.

        Parameters:
            parent(QWidget) the parent widget holding the QComboBo, may
                be empty.
        """
        super().__init__(parent)

        # error Handling
        self.error_frame = None
        self._error = False

        # common stylings
        self.setStyleSheet("combobox-popup: 0;")
        self.setMaxVisibleItems(20)

    def set_error_frame(self, frame: QFrame = None) -> None:
        """Set the related ErrorFrame."""
        self.error_frame = frame

    def focusOutEvent(self, evt: QFocusEvent) -> None:
        """
        Emit the combo box 'activated' signal when the focus is lost.

        Parameters:
            evt (QFocusEvent): event triggered whe the focus is lost
        """
        self.activated.emit(self.currentIndex())
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

    def set_frame(self, frame: ErrorFrame = None) -> None:
        """Set the related ErrorFrame."""
        self.error_frame = frame
