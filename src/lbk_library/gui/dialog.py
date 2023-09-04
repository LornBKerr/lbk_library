"""
Base class for the editing dialog forms.

File:       dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2020 - 2023 Lorn B Kerr
License:    MIT, see file License
"""


from typing import Callable

from PyQt5.QtWidgets import QComboBox, QDialog, QMainWindow, QMessageBox, QWidget

from lbk_library import Dbal, Element


class Dialog(QDialog):
    """
    Base class for the editing dialog forms.

    Holds common functions used by all the editing dialog
    forms.
    """

    # Constants for all dialogs
    VIEW_ELEMENT = 0
    """View an existing element, no editing allowed"""
    ADD_ELEMENT = 1
    """Add a new Element."""
    EDIT_ELEMENT = 2
    """Edit an existing Element."""

    SAVE_NEW = 1
    """Save the form contents, then clear form for new element."""
    SAVE_DONE = 2
    """Save the form contents, then close form."""

    def __init__(self, parent: QMainWindow, dbref: Dbal, operation: int) -> None:
        """
        Initialize the form common elements.

        Parameters:
            parent (QMainWindow): The parent window owning this dialog.
            dbref (Dbal): A reference to the current database
            operation (int): the editing operation, one of ADD_ELEMENT,
                EDIT_ELEMENT or VIEW_ELEMENT.
        """
        super().__init__(parent)

        self.__dbref = dbref
        """The database for this dialog."""
        self.__element = None
        """The element being displayed/processed by the dialog."""
        self.__operation = operation
        """The current editing operation, one of ADD_ELEMENT,
            EDIT_ELEMENT or VIEW_ELEMENT."""
        self.form: QDialog
        """The gui form for this dialog."""

    def get_dbref(self) -> Dbal:
        """
        Get the reference to the current database.

        Returns:
            (Dbal) reference to current database
        """
        return self.__dbref

    def get_element(self) -> Element:
        """
        Get the element for this dialog.

        Returns:
            (Element) the element for this form
        """
        return self.__element

    def set_element(self, element: Element) -> None:
        """
        Set the element for this dialog.

        Parameters:
            element (Element): for this form
        """
        self.__element = element

    def get_operation(self) -> Dbal:
        """
        Get the current editing operation.

        Returns:
            (int) One of ADD_ELEMENT, EDIT_ELEMENT or VIEW_ELEMENT.
        """
        return self.__operation

    def set_operation(self, operation: int = VIEW_ELEMENT) -> None:
        """
        Set the operation for this dialog.

        Parameters:
            operation (int): The current editing operation, one of
                Dialog.ADD_ELEMENT, Dialog.EDIT_ELEMENT or
                Dialog.VIEW_ELEMENT. Default operation is VIEW_ELEMENT
                (i.e. read only)
        """
        if operation in (Dialog.ADD_ELEMENT, Dialog.EDIT_ELEMENT, Dialog.VIEW_ELEMENT):
            self.__operation = operation
        else:
            self.__operation = Dialog.VIEW_ELEMENT

    def set_invalid_indicator(self, widget: QWidget) -> bool:
        """
        Flag the invalid entry in a widget.

        Errors are noted by setting the label to 'Bold' and 'Red'.

        Parameters:
            widget (QWidget): the widget's label to flag.

        Returns:
            (bool) False indicating an invalid entry in a widget
        """
        # used to be 'set_invalid_format()'
        widget_type = str(type(widget))[:-2].rsplit(".", maxsplit=1)[-1]
        font = widget.font()
        font.setBold(True)
        # font.setPointSize(font.pointSize() + 2)
        widget.setFont(font)
        widget.setStyleSheet(widget_type + " {color: red;}")
        return False

    def set_valid_indicator(self, widget: QWidget) -> bool:
        """
        Clear the error indication of the form widget.

        Parameters:
            widget (QWidget) the form widget to flag.

        Returns:
            (bool) True indicating a valid entry.
        """
        # used to be 'set_valid_format()'
        widget_type = str(type(widget))[:-2].rsplit(".", maxsplit=1)[-1]
        font = widget.font()
        font.setBold(False)
        # font.setPointSize(font.pointSize() - 2)
        widget.setFont(font)
        widget.setStyleSheet(widget_type + " {color: black;}")
        return True

    def set_combo_box_selections(
        self, combo_box: QComboBox, selections: list[str], selected: int | None = None
    ) -> None:
        """
        Fill the combo box selection set.

        Add the 'selections' to the combo box, optionally selecting the
        'selected' item if given.

        Paramters:
            combo_box (QComboBox): the combo box to initialize.
            selections (list[str]): available selections.
            selected (str): (Optional) the inital selection.
        """
        combo_box.clear()
        combo_box.addItems(selections)
        combo_box.setCurrentIndex(combo_box.findText(selected))

    def action_cancel(self, save_action: Callable, action: int) -> bool:
        """
        Close the dialog.

        Check if entries have changed. If so, ask if discard or save
        entry and close dialog or stay on dialog.

        Parameters:
            save_action (Callable): the method to save the form
                information
            action (int): type of save action, either Dialog.SAVE_NEW or
                Dialog.SAVE_DONE

        Returns:
            (bool) True if dialog is closed, False if not.
        """
        if self.get_element().have_values_changed():
            msg_box = self.message_question_changed_close("Dialog Entries")
            result = self.message_box_exec(msg_box)
            if result == QMessageBox.StandardButton.Yes:
                if self.get_element().is_element_valid():
                    save_action(action)  # save and close dialog
                    return self.close()
                else:
                    msg_box2 = self.message_warning_invalid("Invalid Entries")
                    result = self.message_box_exec(msg_box2)
                    return False
            elif result == QMessageBox.StandardButton.No:
                return self.close()  # just close dialog
        else:
            return self.close()

    def message_information_close(self, msg_text: str) -> None:
        """
        Display a "Success' message dialog for a form action.

        Parameters:
            msg_text (str): text for message, may be empty string

        Returns:
            (QMessageBox) The 'informational' message box ready for display.
        """
        return QMessageBox(
            QMessageBox.Icon.Information,
            "Success",
            msg_text,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            self,
        )

    def message_question_changed_close(self, changed_name: str) -> None:
        """
        Display a message dialog warning of a form entry change.

        Parameters:
            changed_name (str): the name of the changed form element.

        Return:
            (QMessageBox) The 'changed' message box ready for display.
        """
        return QMessageBox(
            QMessageBox.Icon.Question,
            changed_name + " Changed",
            "Do you want to save the current changes before closing form?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
            | QMessageBox.StandardButton.Cancel,
            self,
        )

    def message_question_changed(self, changed_name: str) -> None:
        """
        Display a message dialog warning of a form entry change.

        Parameters:
            changed_name (str): the name of the changed form element

        Returns:
            (QMessageBox) The 'changed' message box ready for display.
        """
        return QMessageBox(
            QMessageBox.Icon.Question,
            changed_name + " Changed",
            "Do you want to save the current" + " changes before reloading form?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
            | QMessageBox.StandardButton.Cancel,
            self,
        )

    def message_question_no_changes(self) -> None:
        """
        Display a message dialog noting no changes on the form.

        Returns:
            (QMessageBox) The 'warning' message box ready for display.
        """
        return QMessageBox(
            QMessageBox.Icon.Question,
            "Form Entries Have Not Changed",
            "Nothing has changed, so nothing to save",
            QMessageBox.StandardButton.Ok,
            self,
        )

    def message_warning_selection(self, name: str, action: str):
        """
        Display message dialog warning 'name' selection is missing.

        The selection has not been made so the 'action' cannot be
        accomplished.

        Parameters:
            name (str): the selected widget.
            action (str): action to take on selection.

        Returns:
            (QMessageBox) The 'warning' message box ready for display.
        """
        return QMessageBox(
            QMessageBox.Icon.Warning,
            name + " has not been selected",
            "Nothing to " + action,
            QMessageBox.StandardButton.Ok,
            self,
        )

    def message_warning_failed(self, operation: str) -> None:
        """
        Display a message dialog warning of a failed operation.

        Parameters:
            operation (str) the name of the failed operation.

        Returns:
            (QMessageBox) The 'warning' message box ready for display.
        """
        return QMessageBox(
            QMessageBox.Icon.Warning,
            operation + " Operation Failed",
            "The " + operation + " operation failed for some reason.",
            QMessageBox.StandardButton.Ok,
            self,
        )

    def message_warning_invalid(self, msg_text: str = "") -> None:
        """
        Display a message dialog warning of invalid entries on the form.

        Parameters:
            msg_text (str): Text to add to message information, may
                be empty string

        Returns:
            (QMessageBox) The 'warning' message box ready for display.
        """
        text = "Please correct the highlighted errors"
        if msg_text:
            text = text + "\n" + msg_text

        return QMessageBox(
            QMessageBox.Icon.Warning,
            "Form Entries Invalid",
            text,
            QMessageBox.StandardButton.Ok,
            self,
        )

    def message_box_exec(self, message_box: QMessageBox) -> QMessageBox.StandardButton:
        """
        Return the result of executing a prepare message box.

        Parameters:
            message_box (QMessageBox): the box to execute.

        Returns:
            (QMessageBox.StandardButton) the button clicked
        """
        return message_box.exec()
