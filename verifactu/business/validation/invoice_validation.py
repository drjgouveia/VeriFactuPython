"""InvoiceValidation - Validación de facturas según especificaciones AEAT."""

from typing import List


class InvoiceValidation:
    """Validación de una acción de alta o anulación de factura
    según las especificaciones del sistema VERI*FACTU."""

    def __init__(self, invoice_action):
        self._invoice_action = invoice_action

    def get_errors(self) -> List[str]:
        """Devuelve la lista de errores de validación."""
        errors = []

        action = self._invoice_action
        invoice = action.invoice
        registro = action.registro

        if registro is None:
            return ["No se ha establecido el registro de la acción."]

        from verifactu.business.validation.validators.validator_cabecera import (
            ValidatorCabecera)
        from verifactu.business.validation.validators.validator_sistema_informatico import (
            ValidatorSistemaInformatico)
        from verifactu.business.validation.validators.validator_registro_factura import (
            ValidatorRegistroFactura)

        envelope = action.get_envelope()

        errors.extend(ValidatorCabecera.get_errors(envelope.body.registro.cabecera))

        if hasattr(envelope.body.registro, "registro_factura"):
            for registro_factura in envelope.body.registro.registro_factura:
                errors.extend(
                    ValidatorRegistroFactura.get_errors(registro_factura.registro))

        errors.extend(
            ValidatorSistemaInformatico.get_errors(
                getattr(registro, "sistema_informatico", None)))

        return errors
