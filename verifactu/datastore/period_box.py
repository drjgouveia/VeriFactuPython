"""PeriodBox - Base period box."""

from typing import Optional


class PeriodBox:
    """Base period box."""
    
    def __init__(self):
        self.period: str = ""
        self.path: str = ""