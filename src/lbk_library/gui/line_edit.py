"""
Extend QLineEdit handling the focus lost event.

File:       line_edit.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file LICENSE
"""

from PyQt5.QtGui import QFocusEvent
from PyQt5.QtWidgets import QLineEdit, QWidget


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

    def focusOutEvent(self, evt: QFocusEvent) -> None:
        """
        Emit the line edit 'editingFinished' signal when the focus is lost.

        Parameters:
            evt (QFocusEvent): event triggered whe the focus is lost
        """
        if len(self.text()) == 0:
            self.editingFinished.emit()

        super().focusOutEvent(evt)
