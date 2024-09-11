"""
Provides the interface to access and manipulate the table.

This is used to display a 2-dimensional array of strings. There is no
error checking of values and no conversion of types to strings. Those
needs to be done externally.

File:       table_model.py
Author:     Lorn B Kerr
Copyright:  (c) 2024 Lorn B Kerr
License:    MIT, see file LICENSE
"""

from typing import Any

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtGui import QBrush, QColor


class TableModel(QAbstractTableModel):
    """
    Provides access to QTableView derived tables.

    The data for this model is contained in a list of lists of strings.
    The calling program is responsible for translating the program
    native formate to match this data setup.
    """

    def __init__(
        self,
        data_set: list[list[str]],
        header_titles: list[str],
        column_data_names: list[str],
        column_tooltips: list[str],
        column_alignments: list[Qt.AlignmentFlag],
    ) -> None:
        """
        Initialize the TableModel.

        Parameters:
            data_set (list[list[str]]): The information to display in
            the table formatted as a list of lists.
            header_titles (list[str]): The names of the table columns.
            column_tootips {list[str]): The tooltips in column order for
                each column in the table.
        """
        super().__init__()

        self._data_set: list[list[Any]] = data_set
        """The set of Elements to display."""
        self._column_data_names: [str] = column_data_names
        """The set of column data names."""
        self._header_titles: list[str] = header_titles
        """ The set of Header Titles."""
        self._default_column_tooltips: list[str] = column_tooltips
        """The tooltips in column order for each column in the table."""
        self._cell_tooltips: list[list[int, int, str]] = []
        """Tooltips for individual cell (row, col, tooltip)."""
        self._background: QBrush = QBrush(QColor("White"))
        """The standard background for table cells."""
        self._error_background: QBrush = QBrush(QColor(0xF0C0C0))
        """Background indicating an error in the cell contents."""
        self._cell_backgrounds: list[list[int, int, QBrush]] = []
        """Background for individual cell (row, col, color)."""
        self._default_column_alignments = column_alignments
        """The text alignments in column order for each column in the table."""
        self._cell_alignments: list[list[int, int, Qt.AlignmentFlag]] = []
        """The text alignment for individual cell (row, col, AlignmentFlag)."""

    def data(
        self, index: QModelIndex, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole
    ) -> Any:
        """
        Get the entry for the requested row/column.

        Parameters:
            index(QModelIndex): Index to the specific cell requested.
            role (Qt.ItemDataRole): The type of data requested.
                Implemented Qt.ItemDataRole types include:
                    BackgroundRole: set the background color.
                    DisplayRole: item is display only, default value.
                    EditRole: item is editable.
                    ToolTipRole: the item's tooltip.
                    TextAlignmentRole: the alignment of the text.

            Returns:
                (str) The data item requested.
        """
        entry = None
        # handle the situation where number of data columns is less than
        # number of table columns.
        if index.column() >= len(self._column_data_names):
            pass

        elif role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            entry = self._data_set[index.row()][index.column()]

        elif role == Qt.ItemDataRole.ToolTipRole:
            entry = self.get_tooltip(index)

        elif role == Qt.ItemDataRole.BackgroundRole:
            entry = self.get_background(index)

        elif role == Qt.ItemDataRole.TextAlignmentRole:
            entry = self.get_text_alignment(index)

        return entry

    def setData(
        self,
        index: QModelIndex,
        value: Any,
        role: Qt.ItemDataRole = Qt.ItemDataRole.EditRole,
    ) -> bool:
        """
        Set the item at index to value.

        The dataChanged() signal is emitted if the data was successfully
        set.

        Parameters:
            index(QModelIndex): index to the specific row/column requested.
            value (Any): the new value of the data item with type as
                defined in the roles.
            role (Qt.ItemDataRole) the type of data to be set.
                 Implemented types include:
                    BackgroundRole: set the background color (QBrush).
                    DisplayRole: set the item, display only (#str).
                    EditRole: set the item, editable (str).
                    ToolTipRole: Set the tooltip. (str)
                    TextAlignmentRole: Set the alignment of the text
                        (Qt.Alignment).

        Returns:
            (bool) True if successful; otherwise returns False.

        Signals:
            Emits dataChanged signal if set_data() is successful.
        """
        success = False

        # handle the situation where number data columns is less than
        # number of table columns.
        if index.column() >= len(self._column_data_names):
            success = True

        elif role == Qt.ItemDataRole.EditRole or role == Qt.ItemDataRole.DisplayRole:
            self._data_set[index.row()][index.column()] = value
            success = True

        elif role == Qt.ItemDataRole.ToolTipRole:
            # if special tooltip is set, then delete it.
            self.delete_nondefault_entries(index, self._cell_tooltips)
            # if new value is not the default value , add to special list
            if value != self._default_column_tooltips[index.column()]:
                self._cell_tooltips.append([index.row(), index.column(), value])
            success = True

        elif role == Qt.ItemDataRole.BackgroundRole:
            self.delete_nondefault_entries(index, self._cell_backgrounds)
            if value != self._background:
                self._cell_backgrounds.append([index.row(), index.column(), value])
            success = True

        elif role == Qt.ItemDataRole.TextAlignmentRole:
            self.delete_nondefault_entries(index, self._cell_alignments)
            if value != self._default_column_alignments[index.column()]:
                self._cell_alignments.append([index.row(), index.column(), value])
            success = True

        if success:
            self.dataChanged.emit(index, index)
        return success

    def rowCount(self, index: QModelIndex = QModelIndex()) -> int:
        """
        Get the number of rows (elements in the data set).

        Parameters:
            index QModelIndex): index of parent cell, defaults to an
                empty QModelIndex.

        Returns:
            (int) number of rows in table.
        """
        return len(self._data_set)

    def columnCount(self, index=QModelIndex()) -> int:
        """
        Get the number of columns.

        Parameters:
            index (QModelIndex): index of parent cell, defaults to an
                empty QModelIndex.

        Returns:
            (int) number of columns in table.
        """
        return len(self._header_titles)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """
        Set the flags for specific row/column entry to include editable.

        This adds the ItemIsEditable flag to the default settings of
        itemIsSelectable and ItemIsEnabled for all columns except
        'Record Id' and 'Action(s)'.

        Parameters:
            index (QModelIndex): The cell requesting the flags.

        Returns:
            (Qt.ItemFlags) The flags for the specific cell.
        """
        flags = super().flags(index)
        if self._header_titles[index.column()] != "Record Id":
            flags = flags | Qt.ItemFlag.ItemIsEditable
        return flags

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole,
    ) -> str:
        """
        Return the data for the given role and section in the header.

        For horizontal headers, the section number corresponds to the
        column number; for vertical headers, the row number.

        Parameters:
            section (int): the row or column number of the header
            orientation (Qt.Orientation): either Qt.Orientation.Vertical
                or Qt.Orientation.Horizontal
            role (Qt.ItemDataRole:): the specific role being set,
                defaults to Qt.ItemDataRole.DisplayRole

        Returns:
            The current text contents of the header cell.
        """
        entry = None
        if role == Qt.ItemDataRole.DisplayRole and section < self.columnCount():
            entry = self._header_titles[section]

        return entry

    def setHeaderData(
        self,
        section: int,
        orientation: Qt.Orientation,
        value: str,
        role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole,
    ) -> bool:
        """
        Set the data for the given role and section in the header.

        For horizontal headers, the section number corresponds to the
        column number; for vertical headers, the row number.

        Parameters:
            section (int): the row or column number of the header
            orientation (Qt.Orientation): either Qt.Orientation.Vertical
            role (Qt.ItemDataRole:): the specific role being set,
                defaults to Qt.ItemDataRole.DisplayRole

        Returns:
            (bool) True if the header data was successfully changed,
                False otherwise.

        Signals:
            Emits headerDataChanged signal if set is successful.
        """
        success = False
        if role == Qt.ItemDataRole.DisplayRole:
            self._header_titles[section] = value
            success = True
            self.headerDataChanged.emit(orientation, section, section)
        return success

    def insertRows(
        self, row: int, count: int = 1, parent: QModelIndex = QModelIndex()
    ) -> bool:
        """
        Insert one or more rows into the table.

        Parameters:
            row (int): The zero based row number to insert the new rows.
            count (int): the number (1 or greater) of new rows to insert,
                default is 1.
            parent (QModelIndex): The parent node of the row position to
                insert, default is the empty index.
        Returns:
            (bool) True if the insert was successful, False if not.
        """
        success = False
        self.beginInsertRows(parent, row, row + count - 1)
        count_added = 0
        while count_added < count:
            self._data_set.insert(row, [None for i in range(len(self._data_set[0]))])
            count_added += 1
        success = True
        self.endInsertRows()
        return success

    def set_default_background(
        self, background: QBrush = QBrush(QColor("White"))
    ) -> None:
        """
        Set the default cell background.

        Parameters:
            background (QBrush): The cell backround with no errors,
                default is 'white'.
        """
        self._background = background

    def set_default_error_background(
        self, background: QBrush = QBrush(QColor(0xF08080))
    ) -> None:
        """
        Set the default cell error indicating background.

        Parameters:
            background (QBrush): The cell backround with no errors,
                default is 'white'.
        """
        self._error_background = background

    def set_default_column_alignments(self, alignments: list[Qt.AlignmentFlag]) -> None:
        """
        Set the default cell alignment.

        Parameters:
            background (QBrush): The cell backround with no errors,
                default is 'white'.
        """
        for i in range(len(alignments)):
            self._default_column_alignments.append(alignments[i])

    def get_background(self, index: QModelIndex) -> QBrush:
        """
        Get the background for the given cell.

        Parameters:
            index (QModelIndex): the location o fthe cell.

        Returns:
            (QBrush): the color of the cell.
        """
        entry = self._background
        if len(self._cell_backgrounds):
            # check if special background is set.
            for i in range(len(self._cell_backgrounds)):
                if self._cell_backgrounds[i][0] == index.row():
                    if self._cell_backgrounds[i][1] == index.column():
                        entry = self._cell_backgrounds[i][2]
        return entry

    def get_tooltip(self, index: QModelIndex) -> str:
        """
        Get the tooltip for the given cell.

        Parameters:
            index (QModelIndex): the location o fthe cell.

        Returns:
            (str): the tooltip for the cell
        """
        entry = self._default_column_tooltips[index.column()]
        if len(self._cell_tooltips):
            # check if special tooltip is set.
            for i in range(len(self._cell_tooltips)):
                if self._cell_tooltips[i][0] == index.row():
                    if self._cell_tooltips[i][1] == index.column():
                        entry = self._cell_tooltips[i][2]
                        break
        return entry

    def get_text_alignment(self, index: QModelIndex) -> str:
        """
        Get the text alignment for the given cell.

        Parameters:
            index (QModelIndex): the location o  fthe cell.

        Returns:
            (Qt.AlignmentFlag): the test alignment of the cell,
                typically one or more of the Qt.AlignmentFlags ored
                together.
        """
        entry = self._default_column_alignments[index.column()]
        if len(self._cell_alignments):
            # check if special background is set.
            for i in range(len(self._cell_alignments)):
                if self._cell_alignments[i][0] == index.row():
                    if self._cell_alignments[i][1] == index.column():
                        entry = self._cell_alignments[i][2]
                        break
        return entry

    def delete_nondefault_entries(
        self, index: QModelIndex, entries: list[list[int, int, Any]]
    ) -> None:
        """
        Remove all entries for the given index from the entry list.

        Parameters:
            index (QModelIndex): the location of the cell.
            entries (list[list[int, int, Any]]: set of non-default
                entries.
        """
        for i in range(len(entries)):
            if entries[i][0] == index.row() and entries[i][1] == index.column():
                entries.pop(i)
        return entries
