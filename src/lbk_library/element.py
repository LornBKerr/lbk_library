"""
Implement the base class for types of information in the database.

File:       element.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    see License
"""

from copy import deepcopy
from typing import Any

from .dbal import Dbal
from .validate import Validate

class Element:
    """
    This is the base class for types of information in the database.

    Element contains methods to get, add, delete and update information
    in the database. The set_properties() method must be overridden by
    the child classes for the specific type of element being implemented.
    """

    def __init__(
        self, dbref: Dbal, table_name: str, default_values: dict[str, Any] = None
    ) -> None:
        """
        Initialize a new Element object.

        Parameters:
            dbref: (Dbal) reference to the database holding the element
            table_name: (str) database table to search for the element
                values.
            default_values: (dict[str, Any]) the set of default values
                for this element, default is None. If not given,
                built-in defaults of {'record_id': 0, 'remarks': ''}
                will be used.
        """
        self.validate: Validate = Validate()
        """ reference to the Validate class for value validation """
        self._defaults: dict[str, Any] = {"record_id": 0, "remarks": ""}
        """ Default values for the Element """
        self.__dbref: Dbal = dbref
        """ The database instance to use """
        self.__table: str = table_name
        """ The database table for this instance """
        self.__properties: dict[str, Any] = {}
        """ The current values of this instance """
        self.__initial_values: dict[str, Any] = {}
        """ Hold the initial settings of the properties """
        self.__changed_properties: dict[str, bool] = {}
        """ boolean flags of properties changed, updated as entries are
            checked. Flag is set to True if value is changed, False if
            not """
        self.__properties_valid: dict[str, bool] = {}
        """(dict) set of boolean flags of element properties validated,
            each flag is set to False if value is invalid, True if
            value is valid """

        if default_values:  # set the current default values
            self._defaults = default_values
        self.set_initial_values(deepcopy(self._defaults))
        # end __init__()

    def get_properties_from_db(
        self, column_name: str, column_value: Any
    ) -> dict[str, Any]:
        """
        Retrieve the properties of a single element from the database.

        The requested element is selected by the table column name and
        the key column value designated.

        Parameters:
            column_name: (str) within the table containing the key values
            column_value: (Any) Key value requested

        Returns:
            (dict) Row containing requested element if successful or
            an empty dict object if not.
        """
        self.__properties = {}
        if column_name and column_value:
            query = {}
            query["type"] = "SELECT"
            query["table"] = self.__table
            query["keys"] = ["*"]
            query["where"] = (
                column_name + " = " + str(self.__dbref.sql_validate_value(column_value))
            )
            query_sql = self.__dbref.sql_query_from_array(query, {})
            query_result = self.__dbref.sql_query(query_sql, [])

            # get the row, if row not found, returns None
            self.__properties = self.__dbref.sql_fetchrow(query_result)
            if self.__properties is None:
                self.__properties = {}
        return self.__properties
        # end get_properties_from_db()

    def add(self) -> int:
        """
        Add an element to the database.

        Returns:
            (int) unique id of the newly added element or False if
                add failed
        """
        return_value = False
        property_set = self.get_properties()
        del property_set["record_id"]  # new entry id will be assigned
        query = {
            "type": "insert",
            "table": self.get_table(),
        }
        sql = self.get_dbref().sql_query_from_array(query, property_set)
        result = self.get_dbref().sql_query(sql, property_set)
        if result:
            return_value = self.__dbref.sql_nextid(result)
            property_set["record_id"] = return_value

        return return_value
        # end add_element()

    def delete(self) -> bool:
        """
        Delete an element from the database.

        This always uses the record_id column and value to identify
        the record to delete.

        Returns:
            (bool) True if the deletion was successful, False if not.
        """
        return_value = False
        query = {
            "type": "delete",
            "table": self.get_table(),
            "where": "record_id =" + str(self.get_record_id()),
        }
        sql = self.__dbref.sql_query_from_array(query, [])
        result = self.get_dbref().sql_query(sql, [])
        if result:
            return_value = True
        return return_value
        # end delete_element()

    def update(self) -> bool:
        """
        Update an element in the database.

        This always uses the record_id column and value to identify
        the record to update.

        Returns:
            (bool) True if the update was successful, False if not.
        """
        return_value = False
        # get the values to set, assume all but 'record_id'
        property_set = self.get_properties()
        # query the database
        query = {"type": "update", "table": self.get_table()}
        query["where"] = "record_id = " + str(property_set["record_id"])
        sql = self.get_dbref().sql_query_from_array(query, property_set)
        result = self.get_dbref().sql_query(sql, property_set)
        if result:
            return_value = True

        return return_value
        # end update()

    def get_properties(self) -> dict[str, Any]:
        """
        Get the element properties as a dict() of property_names->values.

        Return (dict) The element properties.
        """
        return self.__properties
        # end get_properties()

    def set_properties(self, properties: dict[str, Any]) -> None:
        """
        Set the values of the Element properties array.

        This must be overridden and called by the child class to handle
        the full set of properties. This method sets the common
        properties 'record_id' (contained in all Elements) and
        'remarks' (contained in many Elements).

        Each property is validated for type and value within an
        acceptable range, with unacceptable values set to the
        respective default values. Properties not part of the element
        are discarded.

        Parameters:
            properties: (dict) object holding the element values. Keys
            must match the required keys of the element being modified,
            properties may be sparse.
        """
        if properties is not None and isinstance(properties, dict):
            for key in properties.keys():
                if key == "record_id":
                    self.set_record_id(properties[key])
                elif key == "remarks":
                    self.set_remarks(properties[key])
        # end set_properties()

    def _get_property(self, name: str) -> Any:
        """
        Get an individual property value by Name.

        Parameters:
            name: (str) name of property to retrieve

        Returns:
            (Any) value of property if property is defined.

        Raises:
            KeyError: if name is not a valid property name.
        """
        return self.__properties[name]
        # end _get_property()

    def _set_property(self, name: str, value: Any) -> None:
        """
        Set an individual property.

        This is a low level function with no error checking.

        Parameters:
            name: (str) property name
            value: (Any) value of this property
        """
        self.__properties[name] = value
        # end _set_property()

    def get_record_id(self) -> int:
        """
        Get the Elements's record_id.

        Returns:
            (int) The Elements's record_id or 0 if no record_id is
                assigned
        """
        record_id = self._get_property("record_id")
        if record_id is None:
            record_id = self._defaults["record_id"]
        return record_id
        # end get_record_id()

    def set_record_id(self, record_id: int) -> dict[str, Any]:
        """
        Set the Element's entry index.

        Parameters:
            record_id: (int)  the new record_id for the Element.
                Must be an integer greater than 0 and must be unique
                when Element is stored to the database (not checked).
                If the supplied record_id is not valid, the
                record_id is set to __defaults['record_id'].

        Returns:
            (dict)<br>&emsp;&emsp;['entry'] - (int) the updated
                record_id
            <br>&emsp;&emsp;['valid'] - (bool) True if the operation
                suceeded, False otherwise
            <br>&emsp;&emsp;['msg'] - (str) Error message if not valid
        """
        result = self.validate.integer_field(record_id, self.validate.REQUIRED, 1)
        if result["valid"]:
            self._set_property("record_id", result["entry"])
        else:
            self._set_property("record_id", self._defaults["record_id"])
        self.update_property_flags("record_id", result["entry"], result["valid"])
        return result
        # end set_record_id()

    def get_remarks(self) -> str:
        """
        Get the remarks for this Element.

        Returns:
            (str) The remarks for this Element, the default value if no
            remarks are assigned.
        """
        remarks = self._get_property("remarks")
        if remarks is None:
            remarks = self._defaults["remarks"]
        return remarks
        # end get_remarks()

    def set_remarks(self, remarks: str) -> dict[str, Any]:
        """
        Set the remarks for this Item.

        The remarks are optional and may be empty.

        Parameters:
            remarks: (str) For this Element, may be empty.

        Returns:
        (dict)<br>&emsp;&emsp;['entry'] - the updated remarks for this
            Element
            <br>&emsp;&emsp;['valid'] - (bool) True if the operation
                suceeded, False otherwise
            <br>&emsp;&emsp;['msg'] - (str) Error message if not valid
        """
        if remarks is None:
            remarks = ""
        result = self.validate.text_field(remarks, self.validate.OPTIONAL, 0)
        if result["valid"]:
            self._set_property("remarks", result["entry"])
        else:  # really no way to be here
            self._set_property("remarks", "")
        self.update_property_flags("remarks", result["entry"], result["valid"])
        return result
        # end set_remarks()

    def get_dbref(self) -> Dbal:
        """
        Get the database reference for this element.

        Returns:
            (Dbal) A reference to the current database
        """
        return self.__dbref
        # end get_dbref()

    def get_table(self) -> str:
        """
        Get the name of the database table for the child.

        Returns:
        (str) The table name for this element.
        """
        return self.__table
        # end get_table()

    def get_initial_values(self) -> dict[str, Any]:
        """
        Get the intial values for the element.

        Returns:
            (dict) the initial values assigned to the element's
            properties.
        """
        return self.__initial_values
        # end get_initial_values()

    def set_initial_values(self, initial_value_set: dict[str, Any]) -> None:
        """
        Set the initial settings for the element entries.

        The initial values are set. The changed flags are initialized
        to false. If the record_id is an integer greater than 0, the
        valid flags are initialized to True, otherwise, False.

        Parameters:
            initial_value_set (dict) holds the intial values assigned to
            the element's properties.

        Raises:
            TypeError if 'initial_value_set' is not a dict
        """
        if isinstance(initial_value_set, dict):
            self.__initial_values = deepcopy(initial_value_set)
        else:
            raise TypeError(
                "Initial_value set must be a dict with the initial"
                + " values for the element"
            )
        # end set_initial_values()

    def update_property_flags(self, name: str, value: Any, valid: bool) -> None:
        """
        Update the flags for a property member.

        This updates the change flag and the valid flag for the named
        property member.

        Parameters:
            name: (str) the name of the specific property member
            value: (Any) the new property value
            valid: (bool) True if new value is valid, false if not
        """
        self.set_value_changed_flag(name, value)
        self.set_value_valid_flag(name, valid)
        # end update_property_flags()

    def get_value_changed_flag(self, entry_name: str) -> bool:
        """
        Get an value changed flag for the given property.

        The flag will be True if the property has changed from the
        initial value, False if not.

        Parameters:
            entry_name: (str) name of entry to check

        Returns:
            (bool) The state of the entry changed flag

        Raises:
            KeyError if entry_name is not a valid name
        """
        return self.__changed_properties[entry_name]
        # end get_value_changed_flag()

    def set_value_changed_flag(self, entry_name: str, entry_value: Any) -> bool:
        """
        Set an value changed flag.

        The given value changed flag is set True if the entry value has
        changed from the initial value, False if not.

        Parameters:
            entry_name (str) name of entry that changed
            entry_value: (Any) value of the entry that changed

        Returns:
            (bool) The updated state of the entry changed flag
        """
        self.__changed_properties[entry_name] = (
            self.__initial_values[entry_name] != entry_value
        )
        return self.__changed_properties[entry_name]
        # end set_value_changed_flag()

    def have_values_changed(self) -> bool:
        """
        Check the entry changed flags.

        The result is True if any value changed flag is set, False
        otherwise.

        Returns:
            (bool) True if any entry has changed, False if no entry
                has changed.
        """
        entries_changed = False
        for key in self.__changed_properties:
            if self.__changed_properties[key]:
                entries_changed = True
                break
        return entries_changed
        # end have_values_changed()

    def clear_value_changed_flags(self) -> None:
        """Clear the set of 'value changed' flags."""
        self.__changed_properties.clear()
        # end clear_value_changed_flags()

    def get_value_valid_flag(self, entry_name: str) -> bool:
        """
        Get a value valid flag.

        Parameteres:
            entry_name (str) entry to get validation flag

        Returns:
            (bool) the resulting flag value

        Raises:
            KeyError if entry_name is not in the value valid flag set
        """
        return self.__properties_valid[entry_name]
        # end get_value_valid_flag()

    def set_value_valid_flag(self, entry_name: str, entry_valid: bool) -> bool:
        """
        Set a entry valid flag.

        Parameters:
            entry_name: (str) entry to set validation flag
            entry_valid: (bool) True if entry is valid, False if not

        Returns:
            (bool) the resulting flag value
        """
        self.__properties_valid[entry_name] = entry_valid
        return self.__properties_valid[entry_name]
        # end set_value_valid_flag()

    def is_element_valid(self) -> bool:
        """
        Check the Element validity.

        Implicit here is that all properties have been checked for
        validity. This should be done as part of the element
        construction.

        Returns:
            (bool) True if all element values are valid, False otherwise.

        Raises:
            KeyError if entry_name is not a valid name
        """
        element_valid = True
        if not self.get_properties():
            # Can't be valid if no properties are defined
            element_valid = False
        for key in self.get_properties():
            element_valid = element_valid and self.get_value_valid_flag(key)
        return element_valid
        # end validate_dialog_entries()

    def clear_value_valid_flags(self) -> None:
        """Clear the set of 'valid' flags."""
        self.__properties_valid.clear()
        # end clear_value_valid_flags()

# end Class Element

