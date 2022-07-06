## A Project Library Collection.


This contains common classes that support several of my projects. It covers
common tasks that I found I was writing multiple minor variants frequently.
It is set out in case anyone else may find it useful.

This module contains the following classes
| Class | Description |
| --- | --- |
| Dbal | A database abstraction layer for SQLite3 |
| Element | Base class for types of information in a database |
| ElementSet | Base class for a set of basic elements |
| IniFileParser | Read and Write *.ini Files |
| Validate | Support validation of values going into the database |
|  |  |

Future updates will include supporting classes for dialogs and tables.

The **Dbal** class supplies the required minimum functionality to use the
Sqlite3 database. This is inspired by and modeled on the Dbal of PHPBB 3.1,
much simplified and implemented in python.

The **Element** class abstracts the basic functions to get, add, delete and
update information in the database. The ElementSet is an iterable collection
of Elements. These two class are to be subclassed to handle specific database
collections.

The **Validate** class provides validation functions for Booleans, Dates, Floats,
Integers, and Text fields including minimum and maximum values and if required
or optional.

The **IniFileParser** exposes a stored configuation file (*.ini) as a standard
python dict object using the python configparser library. it provides 2
simple methods to read and write the full ini file and provides a method
to get the config file directory path. It uses the standard
Linux or Windows 10/11 configuration file locations.
