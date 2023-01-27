"""
Implement the base class for sets of types of information in the database.

File:       element_set.py
Author:     Lorn B Kerr
Copyright:  (c) 2022, 2023 Lorn B Kerr
License:    MIT see file License
"""

from collections.abc import Iterator
from typing import Any

from .dbal import Dbal
from .element import Element


class ElementSet:
    """
    The base class for a set of Elements in the database.

    The set of Element types must be all the same type. The class
    implements the "Iterator" interface.
    """

    def __init__(
        self,
        dbref: Dbal,
        table_name: str,
        element_type: type,
        where_column: str = None,
        where_value: Any = None,
        order_by_column: str = None,
        limit: int = None,
        offset: int = None,
    ) -> None:
        """
        Get a list of elements from the database table.

        This will return a list of rows from the database table where
        the 'where_column' contains the 'where_value'. The list can
        optionally be sorted ascending by the values in the
        'order_by_column'.

        The number of rows can be optionally limited to the number of
        rows in 'limit and the search will start at the row number
        (zero based) given in 'offset'.

        Parameters:
            dbref (Dbal): reference to the database holding the element.
            table_name (str): database table to search for the element
                values.
            element_type (type): the type of element in the set,
            where_column (str): The key column of the table containing
                the key value to determine the elements being retrieved.
                If null, all rows are retrieved.
            where_value (Any): The key value to retrieve. Required if
                where_column is set.
            order_by_column (str): one or more column names separated
                by commas to order the resulting set of elements.
            limit (int): number of rows to retrieve, defaults to all.
            offset (int): row number to start retrieval, 0 based,
                defaults to row 0.
        """
        self.__dbref: Dbal = dbref
        """ The database holding the element set """
        self.__table: str = table_name
        """ The database table for this element set """
        self.__property_set: list[Element] = []
        """ The set of elements in this element set """
        self.__position: int = -1
        """ The current iterator position in the property_set, """

        # set the initial query array
        query: dict[str, Any] = {"type": "SELECT", "table": self.__table}

        # case 1 - basic case: get all elements from table
        values: dict[str, Any] = {}
        query["where"] = ""

        # case 2 - selection case: get all elements from table matching
        #    column name and value
        if where_column is not None and where_value is not None:
            query["where"] = where_column + " = :" + where_column
            values[where_column] = where_value

            # case 3 - ordered result: results of case 1 or case 2
            #   ordered by one or more column name(s)
        if order_by_column is not None:
            query["order_by"] = order_by_column

            # case 4 - partial set: results of cases 1, 2 or 3 limited
            #   to a partial result
        if limit:
            query["limit"] = list(str(limit))
            values["limit"] = limit
            if offset:
                query["limit"].append(str(offset))
                values["offset"] = offset

        query_str = self.__dbref.sql_query_from_array(query, values)
        query_result = self.__dbref.sql_query(query_str, values)

        # get the rows, if rows not found, returns empty list
        self.__property_set = self.__dbref.sql_fetchrowset(query_result)

        # convert to a list of 'element_type'
        element_set = list()
        property_set = self.get_property_set()

        for row in property_set:
            element = element_type(self.get_dbref(), row)
            element.set_initial_values(row)
            element.set_properties(row)
            element_set.append(element)
        self.set_property_set(element_set)

    def append(self, element: Element) -> None:
        """
        Append an element to the end of the property set.

        Parameters:
            element (Element): the element to append to the property set
        """
        self.insert(len(self.get_property_set()), element)

    def insert(self, index: int, element: Element) -> None:
        """
        Insert an element into the property set at a specific index.

        Parameters:
            index (int): location to insert the element (zero based)
            element (Element): the element to insert into the
                property set
        """
        self.get_property_set().insert(index, element)

    def get(self, location: int) -> Element:
        """
        Get an element from the property set at the given index.

        Parameters:
            location (int): index of the element to be retrieved
                (zero based)
        """
        return self.get_property_set()[location]

    def delete(self, location: int) -> None:
        """
        Delete an element from the property set at the given index.

        Parameters:
            location (int): index of the element to be deleted
                (zero based)
        """
        del self.get_property_set()[location]

    def get_dbref(self) -> Dbal:
        """
        Get the database reference.

        Returns:
            (Dbal) The database reference for this element set.
        """
        return self.__dbref

    def get_table(self) -> str:
        """
        Get the database table name.

        Returns:
            (str) The table name for this element set.
        """
        return self.__table

    def set_table(self, table: str) -> None:
        """
        Set the database table name.

        Parameters:
            table (str): The table name for this element set.
        """
        self.__table = table

    def get_property_set(self) -> list[Element]:
        """
        Get the property set for this element set.

        Returns:
            (list) The property set for this element set.
        """
        return self.__property_set

    def set_property_set(self, property_set: list[Element]) -> None:
        """
        Set the property set array for this element set.

        Parameters:
            property_set (list): property set for this element set. The
            list may be empty
        """
        if isinstance(property_set, list):
            self.__property_set = property_set
        else:
            self.__property_set = []

    def get_number_elements(self) -> int:
        """
        Get the number of elements in the element set.

        Returns:
            (int) Number of elements in the element set.
        """
        return len(self.get_property_set())

    def build_option_list(self, key: str) -> list[str]:
        """
        Build a list from an element property set.

        This will be for properties such as entry_indices or names for
        use primarily in setting ComboBox selection lists.

        Parameters:
            key (str): the element property to display in the
                option list

        Return:
            (list) List of element properties as strings
        """
        option_list = []
        for element in self.get_property_set():
            option_list.append(str(element.get_properties()[key]))
        return option_list

    # ***** Iterator Interface *****

    def __iter__(self) -> Iterator:
        """
        Generate an Iterator object for this element.

        Returns:
            (Iterator) This ElementSet reference as the Iterator Object.
        """
        return self

    def __next__(self) -> Element:
        """
        Return the next Element in the set.

        Returns:
            (Element) next element in the set

        Raises:
            StopIteration When the last element of the set has been
            returned.
        """
        self.__position += 1
        if self.__position >= len(self.get_property_set()):
            self.__reset__()
            raise StopIteration  # signals "the end"
        return self.get_property_set()[self.__position]

    def __reset__(self) -> None:
        """Reset the iterator position to the beginning."""
        self.__position = -1
