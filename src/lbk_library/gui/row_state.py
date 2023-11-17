"""
The available states of a QTableWidget row.

File:       row_state.py
Author:     Lorn B Kerr
Copyright:  (c) 2023 Lorn B Kerr
License:    MIT, see file LICENSE
"""
from enum import Enum


class RowState(Enum):
    """The available states of a QTableWidget row."""

    NoState = 0
    """The row entries have not been changed."""
    Update = 1
    """The row is flagged by updating."""
    Save = 2
    """The row is flagged by insertion into the database."""
    Delete = 4
    """The row is flagged for deletion."""
