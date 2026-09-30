"""InvoicePeriodReq - Invoice period request."""

from typing import Optional


class InvoicePeriodReq:
    """Invoice period request."""
    
    def __init__(self):
        self.period: str = ""
        self.year: int = 0
        self.month: int = 0