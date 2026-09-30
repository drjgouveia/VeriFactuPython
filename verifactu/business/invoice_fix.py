"""InvoiceFix - Invoice fix/replacement entry."""

from verifactu.business.invoice import Invoice
from verifactu.business.operations.invoice_action import InvoiceAction


class InvoiceFix(InvoiceAction):
    """Invoice fix - fixes a previously sent invoice."""

    def __init__(self, invoice: Invoice):
        super().__init__(invoice)