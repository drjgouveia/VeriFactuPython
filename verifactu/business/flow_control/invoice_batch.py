"""InvoiceBatch - Lote de facturas para envío al API REST."""

from typing import List

from verifactu.business.invoice import Invoice


class InvoiceBatch:
    """Lote de facturas."""

    def __init__(self):
        self.invoices: List[Invoice] = []

    def add(self, invoice: Invoice):
        self.invoices.append(invoice)

    def __len__(self) -> int:
        return len(self.invoices)


# Alias para compatibilidad con el nombre usado por el API REST
InvoicesBatch = InvoiceBatch
