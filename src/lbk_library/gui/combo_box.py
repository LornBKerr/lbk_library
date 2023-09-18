"""
Extend QComboBox to emit the activate signal when the focus is lost.

File:       focus_combo_box.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file LICENSE
"""

from PyQt5.QtGui import QFocusEvent
from PyQt5.QtWidgets import QComboBox, QWidget


class FocusComboBox(QComboBox):
    """Initialize the Focus Combo Box."""

    def __init__(self, parent: QWidget = None) -> None:
        """
        Initialize the Focus Combo Box.

        Parameters:
            parent(QWidget) the parent widget holding the QComboBo, may be
                empty.
        """
        super().__init__(parent)

    def focusOutEvent(self, evt: QFocusEvent) -> None:
        """
        Emit the combo box 'activated' signal when the focus is lost.

        Parameters:
            evt (QFocusEvent): event triggered whe the focus is lost
        """
        self.activated.emit(self.currentIndex())
        super().focusOutEvent(evt)

