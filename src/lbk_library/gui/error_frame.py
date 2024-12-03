"""
Extend QFrame for error indication.

File:       error_frame.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file License
"""


from PySide6.QtCore import Property
from PySide6.QtWidgets import QFrame, QWidget


class ErrorFrame(QFrame):
    """An error indicating frame holding a single widget."""

    def __init__(self, parent: QWidget = None) -> None:
        self._error = False
        """Is the contained entry valid."""

        # style sheets for frame
        self._frame_style_error = "QFrame { border: 2px solid red; border-radius: 0;}"
        self._frame_style_normal = "QFrame { border: 2px white; border-radius: 0;}"

        super().__init__(parent)
        self.setStyleSheet(self._frame_style_normal)

    @Property(bool)
    def error(self) -> bool:
        """Get the error status."""
        return self._error

    @error.setter
    def error(self, value: bool) -> None:
        """Set the error status"""
        self._error = value
        if value:
            self.setStyleSheet(self._frame_style_error)
        else:
            self.setStyleSheet(self._frame_style_normal)
