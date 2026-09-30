"""Document - Data store document."""

from typing import Optional


class Document:
    """Document in the data store."""
    
    def __init__(self):
        self.id: str = ""
        self.data: str = ""
        self.timestamp = None