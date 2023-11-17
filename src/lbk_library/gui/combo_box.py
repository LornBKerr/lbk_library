"""
Extend QComboBox to emit the activate signal when the focus is lost.

Error indication is added thru the use of ErrorFrame.

File:       combo_box.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file LICENSE
"""

from PyQt5.QtCore import pyqtProperty
from PyQt5.QtGui import QFocusEvent
from PyQt5.QtWidgets import QComboBox, QWidget

from .error_frame import ErrorFrame


class ComboBox(QComboBox):
    """Initialize the Combo Box."""

    def __init__(self, parent: QWidget = None) -> None:
        """
        Initialize the Combo Box.

        Parameters:
            parent(QWidget) the parent widget holding the QComboBo, may be
                empty.
        """
        super().__init__(parent)

        # error Handling
        self.error_frame = None
        self._error = False

        # common stylings
        self.setStyleSheet("combobox-popup: 0;")
        self.setMaxVisibleItems(20)

    def focusOutEvent(self, evt: QFocusEvent) -> None:
        """
        Emit the combo box 'activated' signal when the focus is lost.

        Parameters:
            evt (QFocusEvent): event triggered whe the focus is lost
        """
        self.activated.emit(self.currentIndex())
        super().focusOutEvent(evt)

    @pyqtProperty(bool)
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
