"""Settings - Configuration for VeriFactu.

Mirrors the C# `VeriFactu.Config.Settings` static class. Access the
current configuration through the static-style property
``Settings.current`` (equivalent to C# ``Settings.Current``).
"""

import os
import platform
import uuid
from typing import Optional

from verifactu.xml.factu.sistema_informatico import SistemaInformatico
from verifactu.net.rest.api import Api
from verifactu.xml.factu.tipo_huella import TipoHuella
from verifactu.verifactu_end_point_prefixes import VeriFactuEndPointPrefixes

_FILE_NAME = "settings.xml"


def _get_default_path() -> str:
    """Default settings directory, depending on OS."""
    path = os.environ.get("VERIFACTU_PATH", "")
    if path:
        return path
    system = platform.system()
    if system == "Darwin":
        return os.path.join(os.path.expanduser("~"), "Library", "Application Support", "VeriFactu")
    if system == "Windows":
        return os.path.join(os.environ.get("ProgramData", r"C:\ProgramData"), "VeriFactu")
    xdg_data_home = os.environ.get("XDG_DATA_HOME",
                                   os.path.join(os.path.expanduser("~"), ".local", "share"))
    return os.path.join(xdg_data_home, "VeriFactu")


def _get_mac_address() -> Optional[str]:
    try:
        return "%012X" % uuid.getnode()
    except Exception:
        return None


class _SettingsMeta(type):
    """Metaclass providing static-style `Settings.current` access."""

    @property
    def current(cls) -> "Settings":
        if cls._current is None:
            cls.get()
        return cls._current

    @current.setter
    def current(cls, value: "Settings"):
        cls._current = value

    @property
    def path(cls) -> str:
        return cls._path


class Settings(metaclass=_SettingsMeta):
    """Configuración VeriFactu (equivalente de la clase estática Settings de C#)."""

    _current: Optional["Settings"] = None
    _path: str = _get_default_path()
    file_name: str = _FILE_NAME

    blockchain_initialized: bool = False
    event_chain_initialized: bool = False
    event_queue_initialized: bool = False

    def __init__(self):
        self.id_version: str = "1.0"
        self.inbox_path: str = ""
        self.outbox_path: str = ""
        self.blockchain_path: str = ""
        self.event_chain_path: str = ""
        self.invoice_path: str = ""
        self.event_path: str = ""
        self.log_path: str = ""
        self.certificate_serial: str = ""
        self.certificate_thumbprint: str = ""
        self.certificate_path: str = ""
        self.certificate_password: str = ""
        self.veri_factu_end_point_prefix: str = VeriFactuEndPointPrefixes.Test
        self.veri_factu_end_point_req_prefix: str = VeriFactuEndPointPrefixes.TestReq
        self.veri_factu_end_point_validate_prefix: str = VeriFactuEndPointPrefixes.TestValidate
        self.veri_factu_hash_algorithm: TipoHuella = TipoHuella.Sha256
        self.veri_factu_hash_input_encoding: str = "UTF-8"
        self.sistema_informatico: Optional[SistemaInformatico] = None
        self.api: Optional[Api] = None
        self.skip_nif_aeat_validation: bool = True
        self.skip_vies_vat_number_validation: bool = True
        self.logging_enabled: bool = False
        self.disable_blockchain_delete: bool = True
        self.disable_event_chain_delete: bool = True
        self.is_not_verifactu: str = ""

    @classmethod
    def end_point_prefixes(cls, environment: Optional[str] = None):
        """Devuelve los prefijos de endpoint (alta, req, validar)
        correspondientes al entorno indicado: 'test' (por defecto)
        o 'production'."""
        if environment and environment.lower() in ("production", "prod"):
            return (VeriFactuEndPointPrefixes.Production,
                    VeriFactuEndPointPrefixes.ProductionReq,
                    VeriFactuEndPointPrefixes.ProductionValidate)
        return (VeriFactuEndPointPrefixes.Test,
                VeriFactuEndPointPrefixes.TestReq,
                VeriFactuEndPointPrefixes.TestValidate)

    @classmethod
    def get(cls) -> "Settings":
        """Load settings (from disk when supported), or defaults."""
        cls._current = cls._get_default()
        cls._ensure_directories()
        return cls._current

    @classmethod
    def _get_default(cls) -> "Settings":
        """Devuelve un objeto Settings con las opciones por defecto."""
        settings = Settings()

        numero_instalacion = "01"
        try:
            mac = _get_mac_address()
            if mac:
                numero_instalacion = mac
        except Exception:
            pass

        settings.inbox_path = os.path.join(cls._path, "Inbox")
        settings.outbox_path = os.path.join(cls._path, "Outbox")
        settings.blockchain_path = os.path.join(cls._path, "Blockchains")
        settings.event_chain_path = os.path.join(cls._path, "EventChains")
        settings.invoice_path = os.path.join(cls._path, "Invoices")
        settings.event_path = os.path.join(cls._path, "Events")
        settings.log_path = os.path.join(cls._path, "Log")

        sistema_informatico = SistemaInformatico()
        sistema_informatico.nif = "B12959755"
        sistema_informatico.nombre_razon = "IRENE SOLUTIONS SL"
        sistema_informatico.nombre_sistema_informatico = "VeriFactu"
        sistema_informatico.id_sistema_informatico = "01"
        sistema_informatico.version = "1.0.68"
        sistema_informatico.numero_instalacion = numero_instalacion
        sistema_informatico.tipo_uso_posible_solo_verifactu = "N"
        sistema_informatico.tipo_uso_posible_multi_ot = "S"
        sistema_informatico.indicador_multiples_ot = "S"
        settings.sistema_informatico = sistema_informatico

        api = Api()
        api.end_point_create = "https://facturae.irenesolutions.com:8050/Kivu/Taxes/Verifactu/Invoices/Create"
        api.end_point_cancel = "https://facturae.irenesolutions.com:8050/Kivu/Taxes/Verifactu/Invoices/Cancel"
        api.end_point_get_qr_code = "https://facturae.irenesolutions.com:8050/Kivu/Taxes/Verifactu/Invoices/GetQrCode"
        api.end_point_get_sellers = "https://facturae.irenesolutions.com:8050/Kivu/Taxes/Verifactu/Invoices/GetSellers"
        api.end_point_get_records = "https://facturae.irenesolutions.com:8050/Kivu/Taxes/Verifactu/Invoices/GetFilteredList"
        api.end_point_validate_nif = "https://facturae.irenesolutions.com:8050/Kivu/Taxes/Verifactu/Invoices/ValidateNIF"
        api.end_point_get_aeat_invoices = "https://facturae.irenesolutions.com:8050/Kivu/Taxes/Verifactu/Invoices/GetAeatInvoices"
        api.end_point_get_filtered_list = "https://facturae.irenesolutions.com:8050/Kivu/Taxes/Verifactu/Invoices/GetFilteredList"
        api.end_point_create_batch = "https://facturae.irenesolutions.com:8050/Kivu/Taxes/Verifactu/Invoices/CreateBatch"
        api.end_point_validate_nifs = "https://facturae.irenesolutions.com:8050/Kivu/Taxes/Verifactu/Invoices/ValidateNIFs"
        api.end_point_validate_vies_vat_number = "https://facturae.irenesolutions.com:8050/Kivu/Taxes/Verifactu/Invoices/ValidateViesVatNumber"
        api.service_key = "1234"
        settings.api = api

        return settings

    @classmethod
    def _ensure_directories(cls):
        current = cls._current
        if current is None:
            return
        dirs = [cls._path, current.inbox_path, current.outbox_path,
                current.blockchain_path, current.event_chain_path,
                current.invoice_path, current.log_path, current.event_path]
        for d in dirs:
            if d and not os.path.exists(d):
                os.makedirs(d, exist_ok=True)

    @classmethod
    def save(cls):
        """Guarda la configuración en curso (placeholder de serialización)."""
        cls._ensure_directories()

    @classmethod
    def set_config_file_name(cls, file_name: str):
        cls.file_name = file_name
        cls.get()

    @classmethod
    def end(cls):
        """Finaliza los procesos en segundo plano."""
        from verifactu.business.flow_control.invoice_queue import InvoiceQueue
        InvoiceQueue.exit()
        if cls._current and cls._current.is_not_verifactu:
            from verifactu.eventchain.event_queue import EventQueue
            EventQueue.exit()
