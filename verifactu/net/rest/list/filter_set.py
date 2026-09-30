"""Filter set for API queries."""

from typing import List, Optional
from verifactu.net.rest.list.filter import Filter


class FilterSet:
    """Set of filters for API queries."""
    
    def __init__(self):
        self.filters: List[Filter] = []
        self.page: int = 1
        self.page_size: int = 50
        self.sort_field: str = ""
        self.sort_order: str = "ASC"