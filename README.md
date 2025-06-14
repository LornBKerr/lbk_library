## A Project Library Collection.

This contains common classes that support several of my projects. It
covers common tasks that I found I was writing multiple minor variants
frequently. It is set out in case anyone else may find it useful. It has
updated to use PySide6.

This module **lbk_library** contains the following classes:
| Class | Description |
| --- | --- |
| DataFile | Interface to a SQLite3 database file to hold the program data |
| Element | Base class for types of information in a database |
| ElementSet | Base class for a set of basic elements |
| Validate | Support validation of values going into the database |


Package **lbk_library.gui** has the gui related classes:
| Class | Description |
| --- | --- |
| gui.Dialog | Extend QDialog with a number of general support fuctions |
| gui.ErrorFrame | Extend QFrame to provide a selectable empty border or Red border for errors |
| gui.ComboBox | Extend QCombBox to emit the 'activate' signal<BR>on the focus lost event |
| gui.LineEdit | Extend QLineEdit to emit the 'editingFinished' signal<BR>on the focus lost event |
| gui.TableModel | Handle the storage and manipulation of data for a QTableView |
| gui.Settings | Extend QtCore.QSettings to make retrieving a List from settings easier|



The **DataFile** class supplies the required minimum functionality to use
the sqlite3 database. This is inspired by and modeled on the Dbal of
PHPBB 3.1, much simplified and implemented in python.

The **Element** class abstracts the basic functions to get, add, delete
and update information in the database. The **ElementSet** is an
iterable collection of Elements. These two classes are to be subclassed
to handle specific database collections.

The **Validate** class provides validation functions for Booleans,
Dates, Floats, Integers, and Text fields including minimum and maximum
values and if required or optional.

The **IniFileParser** (*Deprecated*, use Settings instead.)
~~exposes a stored configuation file (*.ini) as a
standard python dict object using the python configparser library. It
provides 2 simple methods to read and write the full ini file and
provides a method to get the config file directory path. It uses the
standard Linux or Windows 10/11 configuration file locations by default
or specifc directories if required.~~

The **gui.Dialog** class is the base class extending the QDialog class
with common functionality used by all the project Dilaogs. This includes
the 'record_index' and 'remarks' fields used in all database records,
element default values and validity checks for dialog entries, and a
number of canned message box dialogs.

The **gui.ErrorFrame** class extends the standard QFrame to provide a simple
container for a QLineEdit or QComboBox to indicate an entry error with a
2px Red Border on error without dealing with stylesheets or palette
changes on the contained widget. 

The **gui.ComboBox** class extends the standard QComboBox to include
handling the "FocusOut' event to emit the 'activated' signal to enable
error checking on lost of focus.

The **gui.LineEdit** class extends the standard QLineEdit to include
handling the "FocusOut' event to emit the 'editingFinished' signal to
enable error checking on lost of focus.

The **gui.TableModel** is used to display a 2-dimensional array of
tableview cell information. There is no error checking of values. Each
cell information set is a dict of values for cell value, alignment,
background color, and tooltip.

The **gui.Settings** extends QtCore.QSettings to make saving and
retrieving a List from the QSettings object easier.


