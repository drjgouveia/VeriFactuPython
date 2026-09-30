"""InvoiceCancellation - Anulación de factura."""

from verifactu.business.invoice import Invoice
from verifactu.business.operations.invoice_action import InvoiceAction


class InvoiceCancellation(InvoiceAction):
    """Representa la anulación de una factura previamente remitida."""

    def __init__(self, invoice: Invoice):
        super().__init__(invoice)
        # En la anulación el registro es RegistroAnulacion
        self.registro = self.invoice.get_registro_anulacion()
