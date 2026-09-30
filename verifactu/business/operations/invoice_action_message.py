"""InvoiceActionMessage - Envío del registro al web service de la AEAT."""

import os
import re
from typing import Optional

from verifactu.business.operations.invoice_action_data import InvoiceActionData
from verifactu.config.settings import Settings
from verifactu.xml.namespaces import Items
from verifactu.xml.soap.envelope import Envelope
from verifactu.xml.soap.body import Body
from verifactu.xml.soap.header import Header
from verifactu.xml.soap.header import Header
from verifactu.xml.factu.cabecera import Cabecera
from verifactu.xml.factu.interlocutor import Interlocutor
from verifactu.xml.factu.reg_factu_sistema_facturacion import RegFactuSistemaFacturacion
from verifactu.xml.factu.registro_factura import RegistroFactura
from verifactu.xml.xml_parser import XmlParser

_Action = "?op=RegFactuSistemaFacturacion"


class InvoiceActionMessage(InvoiceActionData):
    """Representa una acción de alta o anulación de registro en todo lo
    referente a su envío al web service de la AEAT y su posterior tratamiento."""

    def __init__(self, invoice):
        super().__init__(invoice)
        self.outbox_path = self.get_out_box_path(self.invoice.seller_id)
        self.inbox_path = self.get_in_box_path(self.invoice.seller_id)
        self._envelope = None
        self._xml = None
        self._response = None
        self._response_envelope = None
        self._response_processed = False

        # Generamos el xml
        self._xml = self.get_xml()

    # ---------------- Métodos internos ----------------

    def get_out_box_path(self, seller_id: str) -> str:
        return self.get_dir_path(os.path.join(Settings.current.outbox_path, seller_id))

    def get_in_box_path(self, seller_id: str) -> str:
        return self.get_dir_path(os.path.join(Settings.current.inbox_path, seller_id))

    def get_invoice_entry_path(self, year: str) -> str:
        return self.get_dir_path(os.path.join(self.outbox_path, year))

    def get_responses_path(self, year: str) -> str:
        return self.get_dir_path(os.path.join(self.inbox_path, year))

    def get_error_response_file_path(self) -> str:
        return os.path.join(
            self.responses_path,
            f"{self.invoice_entry_id}.ERR.{self._now_stamp()}.xml")

    def get_error_invoice_entry_file_path(self) -> str:
        return os.path.join(
            self.invoice_entry_path,
            f"{self.invoice_entry_id}.ERR.{self._now_stamp()}.xml")

    @staticmethod
    def _now_stamp() -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y.%m.%d.%H.%M.%S.%f")

    def get_envelope(self) -> Envelope:
        """Genera el sobre SOAP."""
        obligado = Interlocutor()
        obligado.nombre_razon = self.invoice.seller_name
        obligado.nif = self.invoice.seller_id

        cabecera = Cabecera()
        cabecera.obligado_emision = obligado

        registro_factura = RegistroFactura()
        registro_factura.registro = self.registro

        reg_factu = RegFactuSistemaFacturacion()
        reg_factu.cabecera = cabecera
        reg_factu.registro_factura = [registro_factura]

        envelope = Envelope()
        envelope.header = Header()
        envelope.body = Body(reg_factu)
        return envelope

    def get_xml(self) -> bytes:
        """Devuelve los bytes del XML serializado con los datos actuales."""
        self._envelope = self.get_envelope()
        return XmlParser().get_bytes(self._envelope, Items)

    # ---------------- Envío ----------------

    @staticmethod
    def send_xml_bytes(xml: bytes, op: str = None, certificate=None,
                       is_requirement: bool = False) -> str:
        """Envía un xml en formato binario a la AEAT."""
        if op is None:
            op = _Action

        if is_requirement and not Settings.current.is_not_verifactu:
            raise ValueError("No se puede enviar un registro por requerimiento"
                             " en un sistema configurado como VERI*FACTU.")

        url = (Settings.current.veri_factu_end_point_req_prefix if is_requirement
               else Settings.current.veri_factu_end_point_prefix)

        action = f"{url}{op}"
        from verifactu.net.wsd import Wsd
        return Wsd.call(url, action, xml, certificate)

    def send(self, certificate=None) -> str:
        """Envía el registro a la AEAT."""
        return self.send_xml_bytes(self._xml, self.action, certificate)

    @property
    def action(self) -> str:
        return _Action

    def execute_send(self, certificate=None):
        """Ejecuta el envío del registro."""
        if not self.posted:
            raise ValueError(
                "No se puede enviar un registro no contabilizado (Posted = false).")

        self._response = self.send(certificate)

        # https://github.com/mdiago/VeriFactu/issues/219
        if re.match(r"^<!DOCTYPE html>", self._response):
            from verifactu.common.exceptions import UnexpectedHtmlException
            from verifactu.common.exceptions import SendException
            log_path = Settings.current.log_path
            if log_path:
                os.makedirs(log_path, exist_ok=True)
                html_path = os.path.join(
                    log_path,
                    f"ERR.{self._now_stamp().replace('.', '')}.html")
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(self._response)
            raise SendException(
                "La respuesta recibida de la AEAT no es un XML. Es un documento html.\n"
                "Esto suele ocurrir cuando se utiliza un certificado no válido.")

        self.is_sent = True

    # ---------------- Respuesta ----------------

    def get_response_envelope(self, response: str) -> Envelope:
        """Serializa como sobre soap un string de respuesta de la AEAT."""
        if not response:
            raise ValueError("No existe ninguna respuesta que guardar.")
        return Envelope.from_xml(response)

    def process_response(self, response: Optional[str] = None):
        """Procesa y guarda la respuesta de la AEAT al envío."""
        if response is not None:
            self._response_envelope = self.get_response_envelope(response)

        invoice_entry_file_path = (self.get_error_invoice_entry_file_path()
                                   if not self.csv else self.invoice_entry_file_path)
        response_file_path = (self.get_error_response_file_path()
                              if not self.csv else self.response_file_path)

        # Almaceno xml enviado
        with open(invoice_entry_file_path, "wb") as f:
            f.write(self._xml)

        # Almaceno xml de respuesta
        if self._response:
            with open(response_file_path, "w", encoding="utf-8") as f:
                f.write(self._response)

        # Si la respuesta no ha sido correcta o aceptada con errores renombro archivo
        not_correcto_o_aceptado = self.get_is_not_correcto_o_aceptado()
        if not_correcto_o_aceptado and os.path.exists(self.invoice_file_path):
            os.replace(self.invoice_file_path, self.get_error_invoice_file_path())

        self._response_processed = True

    def get_is_not_correcto_o_aceptado(self) -> bool:
        """Devuelve true si el fichero no está en la AEAT."""
        estado_registro = None
        if (self.error_fault is None and self.respuesta_reg_factu_sistema_facturacion
                and self.respuesta_reg_factu_sistema_facturacion.respuesta_linea):
            estado_registro = (self.respuesta_reg_factu_sistema_facturacion
                               .respuesta_linea[0].estado_registro)

        correcto = self.status == "Correcto"
        aceptado_con_errores = (self.status == "ParcialmenteCorrecto"
                                and estado_registro == "AceptadoConErrores")
        return not (correcto or aceptado_con_errores)

    # ---------------- Propiedades ----------------

    @property
    def invoice_entry_id(self) -> Optional[str]:
        """Identificador del eslabón de la cadena asociado a la factura."""
        if self.registro is None:
            return None
        return str(self.registro.blockchain_link_id or 0).zfill(20)

    @property
    def invoice_entry_path(self) -> Optional[str]:
        if self.registro is None or not self.registro.fecha_hora_huso_gen_registro:
            return None
        return self.get_invoice_entry_path(
            self.registro.fecha_hora_huso_gen_registro[0:4])

    @property
    def responses_path(self) -> Optional[str]:
        if self.registro is None or not self.registro.fecha_hora_huso_gen_registro:
            return None
        return self.get_responses_path(
            self.registro.fecha_hora_huso_gen_registro[0:4])

    @property
    def invoice_entry_file_path(self) -> str:
        return os.path.join(self.invoice_entry_path, f"{self.invoice_entry_id}.xml")

    @property
    def response_file_path(self) -> str:
        return os.path.join(self.responses_path, f"{self.invoice_entry_id}.xml")

    @property
    def envelope(self) -> Optional[Envelope]:
        return self._envelope

    @property
    def xml(self) -> Optional[bytes]:
        return self._xml

    @xml.setter
    def xml(self, value: bytes):
        self._xml = value

    @property
    def response(self) -> Optional[str]:
        return self._response

    @response.setter
    def response(self, value: str):
        self._response = value

    @property
    def response_processed(self) -> bool:
        return self._response_processed

    @property
    def _respuesta(self):
        if self._response_envelope is None:
            return None
        from verifactu.xml.factu.respuesta.respuesta_reg_factu_sistema_facturacion import (
            RespuestaRegFactuSistemaFacturacion)
        registro = self._response_envelope.body.registro
        if isinstance(registro, RespuestaRegFactuSistemaFacturacion):
            return registro
        return None

    @property
    def error_fault(self):
        if self._response_envelope is None:
            return None
        from verifactu.xml.factu.fault.fault import Fault
        registro = self._response_envelope.body.registro
        if isinstance(registro, Fault):
            return registro
        return None

    @property
    def respuestas_reg_factu_sistema_facturacion(self):
        return self._respuesta

    @property
    def error_code(self) -> Optional[str]:
        """Código de error."""
        if self.error_fault is not None:
            return self.error_fault.faultcode
        respuesta = self._respuesta
        if respuesta and respuesta.respuesta_linea:
            return respuesta.respuesta_linea[0].codigo_error_registro
        return None

    @property
    def error_description(self) -> Optional[str]:
        """Descripción del error."""
        if self.error_fault is not None:
            return self.error_fault.faultstring
        respuesta = self._respuesta
        if respuesta and respuesta.respuesta_linea:
            return respuesta.respuesta_linea[0].descripcion_error_registro
        return None

    @property
    def status(self) -> Optional[str]:
        """Estado del envío."""
        respuesta = self._respuesta
        if respuesta is None:
            return None
        return respuesta.estado_envio

    @property
    def csv(self) -> Optional[str]:
        """Código seguro de verificación."""
        respuesta = self._respuesta
        if respuesta is None:
            return None
        return respuesta.csv
