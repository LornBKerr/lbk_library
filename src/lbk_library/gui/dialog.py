"""
Base class for the editing dialog forms.

File:       dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    MIT, see file License
"""

from typing import Callable

from PyQt6.QtCore import Qt
## from PyQt6.QtGui import QColor, QFocusEvent, QPalette
from PyQt6.QtWidgets import (  # QCheckBox,; QComboBox,; QMessageBox,; QWidget,
    QDialog,
    QMainWindow,
)

from ..dbal import Dbal
from ..element import Element


class Dialog(QDialog):
    """
    Base class for the editing dialog forms.

    Holds common values and functions used by all the editing dialog
    forms.
    """

    def __init__(self, parent: QMainWindow, dbref: Dbal) -> None:
        """
        Initialize the form common elements.

        Parameters:
            parent (QMainWindow): The parent window owning this dialog.
            dbref (Dbal): A reference to the current database
        """
        super().__init__(parent)

        # The database for this dialog
        self.__dbref = dbref
        # The element being displayed/processed by the dialog
        self.__element = None
        # end __init__()


    def get_dbref(self) -> Dbal:
        """
        Get the reference to the current database

        Returns:
            (Dbal) reference to current database
        """
        return self.__dbref
        # end get_dbref()


    def get_element(self) -> Element:
        """
        Get the element for this dialog

        Returns:
            (Element) the element for this form
        """
        return self.__element
        # end get_element()


#    def set_element(self, element: Element) -> None:
#        """
#        Set the element for this dialog
#
#        Parameters:
#            element (Element): for this form
#        """
#        self.__element = element
#        # end set_element()
#
#
#    def set_invalid_format(self, widget: QWidget) -> bool:
#        """
#        Flag the invalid entry in a widget by setting the label font to
#        'Bold' and 'Red' and larger.
#
#        Parameters:
#            widget (QWidget): the widget's label to flag.
#
#        Returns:
#            (bool) False indicating an invalid entry in a widget
#        """
#        widget_type = str(type(widget))[:-2].rsplit(".", maxsplit=1)[-1]
#        font = widget.font()
#        font.setBold(True)
#        font.setPointSize(font.pointSize() + 2)
#        widget.setFont(font)
#        widget.setStyleSheet(widget_type + " {color: red;}")
#        return False
#        # end set_invalid_format()
#
#    #
#    # Clear the error indication of the form widget
#    #
#    # @param widget (QWidget) the form widget to flag
#    #
#    # @return (Boolean) True indicating a valid entry.
#    #
#    def set_valid_format(self, widget: QWidget) -> bool:
#        widget_type = str(type(widget))[:-2].rsplit(".", maxsplit=1)[-1]
#        font = widget.font()
#        font.setBold(False)
#        font.setPointSize(font.pointSize() - 2)
#        widget.setFont(font)
#        widget.setStyleSheet(widget_type + " {color: black;}")
#        return True
#        # end set_valid_format()
##
##    def action_cancel(self, save_action: Callable, action: int) -> None:
##        """
##        Close the dialog.
##
##        Check if entries have changed. If so, ask if discard or save
##        entry and close dialog or stay on dialog.
##
##        Parameters:
##            save_action (Callable): the method to save the form
##                information
##        action (int): type of save action, either dialog.SAVE_NEW or
##            dialog.SAVE_DONE
##        """
##        if self.get_element().have_values_changed():
##            result = self.message_question_changed_close("Dialog Entries")
##            if result == QMessageBox.Yes:
##                if self.get_element().is_element_valid():
##                    save_action(action)  # save and close dialog
##                    self.close()
##                else:
##                    self.message_warning_invalid("Invalid Entries")
##            elif result == QMessageBox.No:
##                self.close()  # just close dialog
##        else:
##            self.close()
##
##       # end action_cancel()
##
##    #
##    # Display a "Success' message dialog for a form action
##    #
##    # @param msg_text (String) text for message, may be empty string
##    #
##    # @return (Constant) One of QMessageBox.Yes, QMessageBox.No
##    #
##    def message_information_close(self, msg_text: str) -> None:
##        return QMessageBox(
##            QMessageBox.Information,
##            "Success",
##            msg_text,
##            QMessageBox.Yes | QMessageBox.No,
##            self,
##        ).exec()
##
##    # end message_information_close()
##
##    #
##    # Display a message dialog warning of a form entry change.
##    #
##    # @param changed_name (String) the name of the changed form element
##    #
##    # @return (Constant) One of QMessageBox.Yes, QMessageBox.No, QMessageBox.Cancel
##    #
##    def message_question_changed_close(self, changed_name: str) -> None:
##        return QMessageBox(
##            QMessageBox.Question,
##            changed_name + " Changed",
##            "Do you want to save the current" + " changes before closing form?",
##            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
##            self,
##        ).exec()
##
##    # end message_question_changed_close()
##
##    #
##    # Display a message dialog warning of a form entry change.
##    #
##    # @param changed_name (String) the name of the changed form element
##    #
##    # @return (Constant) One of QMessageBox.Yes, QMessageBox.No, QMessageBox.Cancel
##    #
##    def message_question_changed(self, changed_name: str) -> None:
##        return QMessageBox(
##            QMessageBox.Question,
##            changed_name + " Changed",
##            "Do you want to save the current" + " changes before reloading form?",
##            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
##            self,
##        ).exec()
##
##    # end message_question_changed()
##
##    #    #
##    #    # Display a message dialog warning a 'name' selection has not been made so the
##    #    # 'action' cannot be accomplished.
##    #    # @param name (String) the selection
##    #    # @param action (String) action to take on name
##    #    #
##    #    def message_warning_selection(self, name: str, action: str):
##    #        QMessageBox(QMessageBox.Warning,
##    #                    name + " has not been selected",
##    #                    "Nothing to " + action,
##    #                    QMessageBox.Ok,
##    #                    self).exec()
##    #    # end message_warning_selection()
##    #
##    #    #
##    #    # Display a message dialog warning of a failed operation
##    #    #
##    #    # @param operation (String) the name of the failed operation
##    #    #
##    #    def message_warning_failed(self, operation: str) -> None:
##    #        QMessageBox(QMessageBox.Warning,
##    #                    operation + "Operation Failed",
##    #                    "The " + operation + " operation failed for some reason.",
##    #                    QMessageBox.Ok,
##    #                    self).exec()
##    #    # end message_warning_failed()
##
##    #
##    # Display a message dialog warning of invalid entries on the form.
##    #
##    # @param msg_text (String) Text to add to message information, may be empty string
##    #
##    def message_warning_invalid(self, msg_text: str = "") -> None:
##        text = "Please correct the highlighted errors"
##        if msg_text:
##            text = text + "\n" + msg_text
##
##        QMessageBox(
##            QMessageBox.Warning, "Form Entries Invalid", text, QMessageBox.Ok, self
##        ).exec()
##
##    # end message_warning_invalid()
##
##
##    #
##    # Display a message dialog noting no changes on the form.
##    #
##    def message_question_no_changes(self) -> None:
##        QMessageBox(QMessageBox.Question,
##                    "Form Entries Have Not Changed",
##                    "Nothing has changed, so nothing to save",
##                    QMessageBox.Ok,
##                    self).exec()
##    # end message_question_no_changes()
##
## end class Dialog
