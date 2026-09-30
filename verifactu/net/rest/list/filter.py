"""Filter for API queries."""

from typing import Optional


class Filter:
    """Filter for API queries."""
    
    def __init__(self):
        self.field: str = ""
        self.operation: str = ""
        self.value: str = ""