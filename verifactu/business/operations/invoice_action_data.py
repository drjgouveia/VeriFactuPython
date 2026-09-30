"""InvoiceActionData - Datos de la factura para acciones de alta/anulación."""

import os
from datetime import datetime
from typing import List, Optional

from verifactu.business.invoice import Invoice
from verifactu.common.utils import Utils
from verifactu.config.settings import Settings


class InvoiceActionData:
    """Representa una acción de alta o anulación de registro en todo lo
    referente a los datos de la factura a la que pertenece la acción."""

    def __init__(self, arg):
        """Constructor. Acepta un Invoice o una tupla (invoiceID, invoiceDate, sellerID)."""
        if isinstance(arg, Invoice):
            errors = self.get_arg_errors(arg)
            if errors:
                raise ValueError("\n".join(errors))
            self._invoice = arg
        else:
            invoice_id, invoice_date, seller_id = arg
            if invoice_id is None or seller_id is None:
                raise ValueError(
                    "Los argumentos invoiceID y sellerID no pueden ser nulos.")
            self._invoice = Invoice(invoice_id, invoice_date, seller_id)

        self.invoice_path = self._get_invoice_path(self._invoice.seller_id)
        self.registro = None
        self._posted = False
        self._is_retry_send = False
        self._is_saved = False
        self._is_sent = False

        if isinstance(arg, Invoice):
            self.set_registro()

    # ---------------- Métodos Privados ----------------

    def get_arg_errors(self, invoice: Invoice) -> List[str]:
        """Devuelve una lista con los errores de la factura como argumento."""
        errors = []
        if not invoice.invoice_id:
            errors.append("El objeto Invoice no puede tener como valor de su"
                          " propiedad InvoiceID un valor nulo o una cadena vacía.")
        if not invoice.seller_id:
            errors.append("El objeto Invoice no puede tener como valor de su"
                          " propiedad SellerID un valor nulo o una cadena vacía.")
        if invoice.invoice_date and invoice.invoice_date.year < 2024:
            errors.append("El objeto Invoice no puede tener como valor de su"
                          " propiedad InvoiceDate una fecha de años anteriores al 2024.")
        return errors

    def get_dir_path(self, directory: str) -> str:
        """Devuelve el path de un directorio. Si no existe lo crea."""
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        return directory

    def _get_invoice_path(self, seller_id: str) -> str:
        return self.get_dir_path(os.path.join(Settings.current.invoice_path, seller_id))

    def get_invoice_posted_path(self, year: str) -> str:
        return self.get_dir_path(os.path.join(self.invoice_path, year))

    def get_error_invoice_file_path(self) -> str:
        return os.path.join(
            self.invoice_posted_path,
            f"{self.encoded_invoice_id}.ERR.{datetime.now().strftime('%Y.%m.%d.%H.%M.%S.%f')}.xml")

    # ---------------- Propiedades ----------------

    @property
    def encoded_invoice_id(self) -> str:
        """Identificador de la factura en formato hexadecimal."""
        return Utils.get_encoded_to_hex(self._invoice.invoice_id)

    @property
    def invoice_posted_path(self) -> str:
        return self.get_invoice_posted_path(str(self._invoice.invoice_date.year))

    @property
    def invoice_file_path(self) -> str:
        """Path de la factura en el directorio de facturas."""
        return os.path.join(self.invoice_posted_path, f"{self.encoded_invoice_id}.xml")

    @property
    def invoice(self) -> Invoice:
        return self._invoice

    @property
    def seller_id(self) -> str:
        return self._invoice.seller_id

    @property
    def posted(self) -> bool:
        return self._posted

    @posted.setter
    def posted(self, value: bool):
        self._posted = value

    @property
    def is_retry_send(self) -> bool:
        return self._is_retry_send

    @property
    def is_saved(self) -> bool:
        return self._is_saved

    @is_saved.setter
    def is_saved(self, value: bool):
        self._is_saved = value

    @property
    def is_sent(self) -> bool:
        return self._is_sent

    @is_sent.setter
    def is_sent(self, value: bool):
        self._is_sent = value

    def set_registro(self):
        """Establece el registro relativo a la entrada a contabilizar y enviar."""
        self.registro = self._invoice.get_registro_alta()

    def __str__(self) -> str:
        return (f"{self._invoice.seller_id}-{self._invoice.invoice_id}"
                f"-{self._invoice.invoice_date:%d/%m/%Y}")
