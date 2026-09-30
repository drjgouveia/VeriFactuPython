"""InvoiceEntry - Entrada de factura en el sistema."""

from verifactu.business.invoice import Invoice
from verifactu.business.operations.invoice_action import InvoiceAction


class InvoiceEntry(InvoiceAction):
    """Representa una entrada de factura en el sistema."""

    def __init__(self, invoice: Invoice):
        super().__init__(invoice)
