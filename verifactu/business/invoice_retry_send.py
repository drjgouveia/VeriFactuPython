"""InvoiceRetrySend - Retry sending invoices."""

from typing import Optional


class InvoiceRetrySend:
    """Retry sending invoices."""
    
    def __init__(self):
        self.retry_count: int = 0
        self.retry_delay: int = 60
        self.max_retries: int = 3