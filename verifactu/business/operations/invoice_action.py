"""InvoiceAction - Acción de alta o anulación de registro con validaciones."""

import os
from typing import List

from verifactu.business.operations.invoice_action_post import InvoiceActionPost
from verifactu.xml.factu.alta.causa_exencion import CausaExencion


class InvoiceAction(InvoiceActionPost):
    """Representa una acción de alta o anulación de registro en todo lo
    referente a la factura, su envío a la AEAT y su gestión contable
    en la cadena de bloques."""

    def __init__(self, invoice):
        super().__init__(invoice)
        # Validamos
        errors = self.get_bus_errors()
        if errors:
            raise ValueError("\n".join(errors))

    # ---------------- Validaciones ----------------

    def get_invoice_validation_errors(self) -> List[str]:
        """Devuelve errores de las validaciones de negocio."""
        from verifactu.business.validation.invoice_validation import InvoiceValidation
        validation = InvoiceValidation(self)
        return validation.get_errors()

    def _get_tax_item_validation_errors(self, tax_item) -> List[str]:
        """Errores de la línea de impuesto por reglas de negocio."""
        errors = []
        if tax_item.tax_exception != CausaExencion.NA:
            total = (tax_item.tax_rate + tax_item.tax_amount
                     + tax_item.tax_rate_surcharge + tax_item.tax_amount_surcharge)
            if total != 0:
                errors.append(
                    f"Taxitem [{tax_item}] con TaxException asignada"
                    f" '{tax_item.tax_exception}' no puede tener un valor distinto"
                    " de 0 en las propiedades TaxRate, TaxAmount, TaxRateSurcharge"
                    " y TaxAmountSurcharge.")
        return errors

    def get_tax_items_validation_errors(self) -> List[str]:
        """Errores de las líneas de impuesto por reglas de negocio."""
        errors = []
        if self.invoice.tax_items:
            for tax_item in self.invoice.tax_items:
                errors.extend(self._get_tax_item_validation_errors(tax_item))
        return errors

    def get_bus_errors(self) -> List[str]:
        """Devuelve una lista con los errores de la factura por el
        incumplimiento de reglas de negocio."""
        errors = []

        if os.path.exists(self.invoice_file_path):
            errors.append(
                f"Ya existe una entrada con SellerID: {self.invoice.seller_id}"
                f" en el año {self.invoice.invoice_date.year}"
                f" con el número {self.invoice.invoice_id}.")

        if not self.invoice.seller_name:
            errors.append(
                "Es necesario que la propiedad Invoice.SellerName tenga un valor.")

        # Límite listas
        if self.invoice.rectification_items and len(self.invoice.rectification_items) > 1000:
            errors.append("Invoice.RectificationItems.Count no puede ser mayor de 1.000.")

        if self.invoice.tax_items and len(self.invoice.tax_items) > 12:
            errors.append("Invoice.TaxItems.Count no puede ser mayor de 12.")

        errors.extend(self.get_tax_items_validation_errors())
        errors.extend(self.get_invoice_validation_errors())

        return errors
