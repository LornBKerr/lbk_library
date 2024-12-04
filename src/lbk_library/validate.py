"""
Validate types of information in the database.

File:       validate.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    see License
Version:    1.0.1"""

import datetime
import re
import sys
from typing import Any, Union

file_version = "1.1.0"
changes = {
    "1.0.0": "Initial release",
    "1.0.1": "Added Version Info."
}


class Validate:
    """
    Provides various methods to validate variables.

    Validations are provided for Booleans, Dates, Floats, Integers,
    Text fields and arbitrary regular expressions.
    """

    REQUIRED = True
    """(bool) variable required, must satisfy requirements."""
    OPTIONAL = False
    """(bool) variable optional, if present, must satisfy requirements."""

    def integer_field(
        self,
        value: Union[int, str],
        required: bool,
        min_value: int = 0,
        max_value: int = sys.maxsize,
    ) -> dict[str, Any]:
        """
        Validate a integer numeric field.

        The 'value' can be provided as a integer number or a string
        representation of an integer number.

        If the value is REQUIRED, the value must be present and a valid
        integer value or a string convertable to a integer. The empty
        string is not accepted as valid.

        If the value is OPTIONAL, the value must be present and be a
        valid integer value or a string convertable to a integer; the
        empty string ("") is accepted and converted  to int(0).

        Parameters:
            value (int | str): number to be checked, an integer, a
                string representation of an integer, or "". The empty
                string is only accepted if the value is optional.
            required (bool): one of the constants Validate.REQUIRED or
                Validate.OPTIONAL.
            min_value (int): minimum integer value, default is 0.
            max_value (int): maximum integer value, default is the
                system maximum value for an int.

        Returns:
            (dict)
                ['entry'] - the inital value to be validated.
                ['valid'] - (bool) True if the operation suceeded,
                    False otherwise.
                ['msg'] - (str) Error message if not valid.
        """
        result = {
            "entry": value,  # start with entered value
            "valid": True,  # assume success
            "msg": "",
        }  # with no error message

        if not isinstance(value, (int, str)):
            result["valid"] = False
            result["msg"] = (
                "Value must be a valid integer value or string"
                + " represention of a valid integer value"
            )

        if value == "":
            if required == self.OPTIONAL:
                value = 0
                result["entry"] = value
            else:
                result["valid"] = False
                result["msg"] = "An integer entry is required"

        if isinstance(value, str):
            # remove any leading or training white space
            value = value.strip()
            if re.match(r"^[-+]?([1-9]\d*|0)$", value):
                value = int(value)
                result["entry"] = value
            else:
                result["valid"] = False
                result["msg"] = "Value does not represent an Integer value"

        if result["valid"]:
            if value < min_value:
                result["valid"] = False
                result["msg"] = (
                    "The entry is less than the required"
                    + " minimum value of "
                    + str(min_value)
                )
            elif value > max_value:
                result["valid"] = False
                result["msg"] = (
                    "The entry is greater than the required"
                    + " maximum value of "
                    + str(max_value)
                )
        return result

    def float_field(self, value, required, min_value=-1.0e8, max_value=1.0e8):
        """
        Validate a float numeric field.

        The 'value' can be provided as a float number or a string
        representation of a float number.

        If the value is REQUIRED, the value must be present and a valid
        float value or a string convertable to a float. The empty string
        is not accepted as valid.

        If the value is OPTIONAL, the value must be present and a valid
        float value or a string convertable to a float; the empty string
        ("") is accepted and converted to float(0).

        Parameters:
            value (int): number to be checked, an integer, a string
                representation of an integer, or "". The empty string is
                only accepted if the value is optional.
            required (bool): one of the constants Validate.REQUIRED or
                Validate.OPTIONAL constants
            min_value (float): the minimum acceptable value, default is
                float(-100,000,000.0)
            max_value (float): the maximum acceptable value, default is
                float(+100,000,000.0)

        Returns:
            (dict)
                ['entry'] - the inital value to be validated.
                ['valid'] - (bool) True if the operation suceeded,
                    False otherwise.
                ['msg'] - (str) Error message if not valid.
        """
        result = {
            "entry": value,  # start with entered value
            "valid": True,  # assume success
            "msg": "",
        }

        if not isinstance(value, (float, str)):
            result["valid"] = False
            result["msg"] = (
                "Value must be a valid float value or string"
                + " represention of a valid float value"
            )

        if value == "":
            if required == self.OPTIONAL:
                value = float(0)
                result["entry"] = value
            else:
                result["valid"] = False
                result["msg"] = "An float entry is required"

        if isinstance(value, str):
            # remove any leading or training white space
            value = value.strip()
            if re.match(r"^[+-]?\ *(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$", value):
                value = float(value)
                result["entry"] = value
            else:
                result["valid"] = False
                result["msg"] = "Value does not represent a Float value"

        if result["valid"]:
            if value < min_value:
                result["valid"] = False
                result["msg"] = (
                    "The entry is less than the required"
                    + " minimum value of "
                    + str(min_value)
                )
            elif value > max_value:
                result["valid"] = False
                result["msg"] = (
                    "The entry is greater than the required"
                    + " maximum value of "
                    + str(max_value)
                )
        return result

    def text_field(
        self, text: str, required: bool, min_length: int = 1, max_length: int = 255
    ) -> dict[str, Any]:
        """
        Validate a text field.

        The field needs a valid alphnumeric string, and optional minimum
        and maximum lengths of the field. Default values of 1 and 255
        are supplied for the minimum and maximum lengths. If the entry
        is marked as required, the entry must be present and match the
        length parameters. If not rquired (required = OPTIONAL), then
        the entry may be empty. If not empty, it must match the length
        parameters.

        The entered value should have all HTML tags including script
        tags and comments removed and all whitespace at the front and
        back of the string removed.

        Parameters:
            text (str): test to be checked.
            required (bool): one of the constants Validate.REQUIRED or
                Validate.OPTIONAL constants
            min_length: (int) minimum length in characters, optional,
                default is 1.
            max_length: (int) maximum length in characters, optional,
                default is 255.

        Returns:
            (dict)
                ['entry'] - the inital value to be validated.
                ['valid'] - (bool) True if the operation suceeded,
                    False otherwise.
                ['msg'] - (str) Error message if not valid.
        """
        result = {
            "entry": text,  # start with empty text value
            "valid": True,  # assume success
            "msg": "",
        }

        if not isinstance(text, str):
            result["valid"] = False
            result["msg"] = "Value must be a valid string of text"

        if result["valid"] and required == self.REQUIRED and text == "":
            # required and empty
            result["valid"] = False
            result["msg"] = (
                "A text value ("
                + str(min_length)
                + " and "
                + str(max_length)
                + " characters long) is required and cannot be empty"
            )

            # check the length of the entry
        if result["valid"]:
            text = text.strip()  # remove leading and trailing whitespace
            if len(text) < min_length:
                result["valid"] = False
                result["msg"] = (
                    "The entered value is too short ( at least "
                    + str(min_length)
                    + " characters required)"
                )

            elif len(text) > max_length:
                result["valid"] = False
                result["msg"] = (
                    "The entered value is too long (no more than "
                    + str(max_length)
                    + " characters allowed)"
                )
        return result

    def boolean(self, state: Union[str, int, bool]) -> dict[str, Any]:
        """
        Validate a boolean value.

        This will handle pure boolean values (True or False, 'true' or
        'false') or the value of an expression or widget widget that
        yields either 0 (false) or 1 (true), or the result of some
        operation that yields "on" or 'off".

        Parameters:
            state: (Any) of the boolean to be checked. A (bool) True,
                (str)g 'true', (str) '1', (int) 1, or (str) 'on' are
                accepted as True and (bool) False,  (str) 'false',
                (str) '0', (int) 0 or (str) 'off' are accepted as False.

        Returns:
            (dict)
                ['entry'] - the inital value to be validated.
                ['valid'] - (bool) True if the operation suceeded,
                    False otherwise.
                ['msg'] - (str) Error message if not valid.
        """
        # initialize results array
        result = {
            "entry": 0,  # start with empty check box value
            "valid": True,  # assume success
            "msg": "",
        }  # with no error message

        if state in (True, "true", "on", "1", 1):
            result["entry"] = True
        elif state in (False, "false", "off", "0", 0):
            result["entry"] = False
        else:  # error in entry
            result["valid"] = False
            result["msg"] = "Invalid entry for boolean"

        return result

    def date_field(self, date_input: str, required: bool) -> dict[str, Any]:
        """
        Validate a date field.

        The field is a string representing a date. the representations
        accepted are:
            mm/dd/yyyy such as '02/23/2015' or '2/3/2003'
            yyyy-mm-dd such as '2015-23-03'
            'Feb 23, 2015'  (not Implemented)
            '23 Feb, 2015'(not Implemented)

        Parameters:
            date_input: (str) date to be checked, may be an empty string
                if not REQUIRED
            required (bool): one of the constants Validate.REQUIRED or
                Validate.OPTIONAL constants

        Returns:
            (dict)
                ['entry'] - the inital value to be validated.
                ['valid'] - (bool) True if the operation suceeded,
                    False otherwise.
                ['msg'] - (str) Error message if not valid.
        """
        result = {
            "entry": date_input,  # start with supplied value
            "valid": True,  # assume success
            "msg": "",
        }

        if not isinstance(date_input, str):  # string can be empty
            result["valid"] = False
            result["msg"] = "Value must be a valid string"
        else:
            date_input = date_input.strip()

        if result["valid"]:
            if date_input == "":
                if required == self.REQUIRED:  # required and empty
                    result["valid"] = False
                    result["msg"] = "A date value is required" " and cannot be empty"

        # The string input is converted to a date object and validated
        # to be a valid date.
        if result["valid"]:
            # build a datatime object to check things
            # mm/dd/yyyy; month and day either single or double digits
            if re.match(r"\d{1,2}/\d{1,2}/\d\d\d\d", date_input):
                date_array = date_input.split("/")
                try:
                    date_stamp = datetime.datetime(
                        int(date_array[2]), int(date_array[0]), int(date_array[1])
                    ).timestamp()
                except ValueError:
                    result["entry"] = date_input
                    result["valid"] = False
                    result["msg"] = (
                        date_input + " is not a valid date of form 02/23/2014"
                    )

                # yyyy-mm-dd    month and day either single or double digits
            elif re.match(r"\d\d\d\d-\d{1,2}-\d{1,2}", date_input):
                date_array = date_input.split("-")
                try:
                    date_stamp = datetime.datetime(
                        int(date_array[0]), int(date_array[1]), int(date_array[2])
                    ).timestamp()
                except ValueError:
                    result["entry"] = date_input
                    result["valid"] = False
                    result["msg"] = (
                        date_input + " is not a valid date of form 2015-23-03"
                    )

                # Bad entry
            else:
                result["entry"] = date_input
                result["valid"] = False
                result["msg"] = date_input + " is not recognizable as a valid date"
        return result

    def reg_exp_field(
        self, entry_value: str, reg_exp: str, required: bool
    ) -> dict[str, Any]:
        """
        Validate an entry_value defined by a regular expression.

        This will match an entry_value against a given regular
        expression and return a standard validation result set. The
        reg_exp value must be a valid regular expression with all
        special characters handled (normally a raw string such as
        r"some pattern".

        Parameters:
            value (str): The entry_value to be validated.
            reg_exp (str): The regular expression to be matched.
            required (bool): one of the constants Validate.REQUIRED or
                Validate.OPTIONAL constants

        Returns:
            (dict)
                ['entry'] - the inital value to be validated.
                ['valid'] - (bool) True if the operation suceeded,
                    False otherwise.
                ['msg'] - (str) Error message if not valid.
        """
        result = {
            "entry": entry_value,  # start with supplied value
            "valid": True,  # assume success
            "msg": "",
        }

        try:
            pattern = re.compile(reg_exp)
        finally:
            pass

        if not isinstance(entry_value, str):
            result["valid"] = False
            result["msg"] = "The entry value must be a valid string"

        if result["valid"]:
            if required == self.REQUIRED and entry_value == "":
                result["valid"] = False
                result["msg"] = "Value must be supplied"

            if required == self.REQUIRED and not re.match(reg_exp, entry_value):
                result["valid"] = False
                result["msg"] = "Value format is incorrect."
        return result
