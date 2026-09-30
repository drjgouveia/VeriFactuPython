"""Base Registro class for VeriFactu XML records."""

from datetime import datetime
from typing import Optional

from verifactu.common.utils import Utils
from verifactu.config.settings import Settings
from verifactu.xml.xml_parser import get_xml_date, get_xml_date_time_iso8601
from verifactu.xml.namespaces import NamespaceSF


class Registro:
    """Base class for VeriFactu records: Alta, cancellation, event, etc."""

    def __init__(self):
        self._id_version: str = ""
        self._id_factura = None
        self._fecha_hora_huso_gen_registro: str = ""
        self._huella: str = ""
        self._encadenamiento = None
        self._blockchain_link_id: int = 0

    @property
    def id_version(self) -> str:
        return self._id_version

    @id_version.setter
    def id_version(self, value: str):
        self._id_version = value

    @property
    def id_factura(self):
        return self._id_factura

    @id_factura.setter
    def id_factura(self, value):
        self._id_factura = value

    @property
    def fecha_hora_huso_gen_registro(self) -> str:
        return self._fecha_hora_huso_gen_registro

    @fecha_hora_huso_gen_registro.setter
    def fecha_hora_huso_gen_registro(self, value: str):
        self._fecha_hora_huso_gen_registro = value

    @property
    def huella(self) -> str:
        return self._huella

    @huella.setter
    def huella(self, value: str):
        self._huella = value

    @property
    def encadenamiento(self):
        return self._encadenamiento

    @encadenamiento.setter
    def encadenamiento(self, value):
        self._encadenamiento = value

    @property
    def blockchain_link_id(self) -> int:
        return self._blockchain_link_id

    @blockchain_link_id.setter
    def blockchain_link_id(self, value: int):
        self._blockchain_link_id = value

    @property
    def extern_key(self) -> Optional[str]:
        if self._blockchain_link_id == 0:
            return None
        return str(self._blockchain_link_id).zfill(20)

    def get_hash_text_input(self) -> str:
        """Cadena de entrada para el cálculo del hash."""
        raise NotImplementedError(
            "La clase base Registro no implementa el método get_hash_text_input."
            " Este método debe implementarse en las clases derivadas.")

    def get_hash_input(self) -> bytes:
        text_input = self.get_hash_text_input()
        return Utils.encoding_encode(text_input)

    def get_hash_output(self) -> str:
        hash_bytes = Utils.compute_hash(self.get_hash_input())
        return hash_bytes.hex().upper()

    def get_url_validate(self) -> str:
        url_params = self.get_validate_url_params()
        return f"{Settings.current.veri_factu_end_point_validate_prefix}?{url_params}"

    def get_validate_qr(self) -> bytes:
        content = self.get_url_validate()
        from verifactu.qrcode.qrcode_extensions import get_qr_bytes
        return get_qr_bytes(content)

    def get_validate_url_params(self) -> str:
        raise NotImplementedError("Subclasses must implement get_validate_url_params")

    def set_extern_key(self):
        raise NotImplementedError("SetExternKey not implemented for base Registro.")

    def __str__(self) -> str:
        return f"{self._id_factura}"