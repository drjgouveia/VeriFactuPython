"""InvoiceActionPost - Contabilización en la cadena de bloques y envío."""

from threading import Lock

from verifactu.business.operations.invoice_action_message import InvoiceActionMessage
from verifactu.config.settings import Settings


class InvoiceActionPost(InvoiceActionMessage):
    """Representa una acción de alta o anulación de registro en todo lo
    referente a su gestión contable en la cadena de bloques."""

    def __init__(self, invoice):
        super().__init__(invoice)
        self._locker = Lock()
        from verifactu.blockchain.blockchain import Blockchain
        self.blockchain_manager = Blockchain.get(self.invoice.seller_id)

    # ---------------- Contabilización ----------------

    def post(self, certificate=None):
        """Contabiliza una entrada.

        1. Incluye el registro en la cadena de bloques.
        2. Recalcula Xml con la info Blockchain actualizada.
        3. Guarda el registro en disco en el directorio de registros emitidos.
        4. Establece Posted = true.
        """
        self.blockchain_manager.add(self.registro)
        self.save_blockchain_changes(certificate)

    def save_blockchain_changes(self, certificate=None):
        """Actualiza los datos tras la incorporación del registro a la cadena."""
        if not self.registro.blockchain_link_id:
            raise ValueError(f"El registro {self.registro}"
                             " no está incluido en la cadena de bloques.")
        if self.posted:
            raise ValueError(f"La operación {self} ya está contabilizada.")

        if Settings.current.is_not_verifactu:
            # En NO VERI*FACTU almacenamos el registro firmado.
            from verifactu.noverifactu.signature.signer import Signer
            signer = Signer(certificate)
            self.xml = signer.sign(self.registro)
        else:
            # En VERI*FACTU regeneramos el Xml con la información actualizada.
            self.xml = self.get_xml()

        with open(self.invoice_file_path, "wb") as f:
            f.write(self.xml)

        self.posted = True

    def clear_post(self):
        """Deshace cambios de guardado eliminando el elemento de la cadena
        de bloques (si DisableBlockchainDelete = false) y marcando los
        archivos relacionados como erróneos."""
        import os
        from verifactu.common.exceptions import ClearPostException
        undo_exception = None
        try:
            with self._locker:
                if not Settings.current.disable_blockchain_delete:
                    self.blockchain_manager.delete(self.registro)

                if os.path.exists(self.invoice_entry_file_path):
                    os.replace(self.invoice_entry_file_path,
                               self.get_error_invoice_entry_file_path())

                if os.path.exists(self.invoice_file_path):
                    os.replace(self.invoice_file_path,
                               self.get_error_invoice_file_path())

                self.posted = False
        except Exception as ex:
            undo_exception = ex

        if undo_exception is not None:
            raise ClearPostException(str(undo_exception)) from undo_exception

    def execute_post(self, certificate=None):
        """Ejecuta la contabilización del registro."""
        from verifactu.common.exceptions import PostException
        from verifactu.net.wsd import Wsd

        cert = certificate or Wsd.get_checked_certificate()
        post_exception = None
        try:
            with self._locker:
                self.post(cert)
        except Exception as ex:
            post_exception = ex

        if post_exception is not None:
            raise PostException(str(post_exception)) from post_exception

    # ---------------- Guardado ----------------

    def save(self, certificate=None):
        """Contabiliza y envía a la AEAT el registro."""
        from verifactu.common.exceptions import SendException
        from verifactu.net.wsd import Wsd

        if self.is_saved:
            raise ValueError("El objeto InvoiceEntry sólo"
                             " puede llamar al método Save() una vez.")

        cert = certificate or Wsd.get_checked_certificate()

        send_exception = None

        self.execute_post(cert)

        # En NO VERI*FACTU el registro se almacena localmente
        # y no se remite a la AEAT.
        if Settings.current.is_not_verifactu:
            self.is_saved = True
            return

        try:
            self.execute_send(cert)
            self.process_response()
        except Exception as ex:
            send_exception = ex
            self.clear_post()

        if not self.csv or send_exception is not None:
            if send_exception is None:
                self.clear_post()

        if send_exception is not None:
            raise SendException(str(send_exception)) from send_exception

        self.is_saved = True
