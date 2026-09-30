"""InvoiceQuery - Query for invoices."""

from typing import Optional


class InvoiceQuery:
    """Query for invoices."""

    def __init__(self):
        self.seller_id: str = ""
        self.invoice_id: str = ""
        self.invoice_date = None