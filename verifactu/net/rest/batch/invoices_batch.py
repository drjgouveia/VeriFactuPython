"""Invoices batch for API."""

from typing import List, Optional
from verifactu.business.invoice import Invoice


class InvoicesBatch:
    """Batch of invoices for API operations."""
    
    def __init__(self):
        self.invoices: List[Invoice] = []
        self.service_key: str = ""