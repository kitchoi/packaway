""" This module contains violation data classes.
"""


class ImportRuleViolation:
    """ An object to represent an import violation."""

    def __init__(self, lineno, col_offset, message):
        self.lineno = lineno
        self.col_offset = col_offset
        self.message = message

    def __repr__(self):
        return (
            "ImportRuleViolation("
            f"lineno={self.lineno}, "
            f"col_offset={self.col_offset}, "
            f"message={self.message}"
            ")"
        )
