"""VeriFactu - Python 3.14 port of the VeriFactu .NET library.

Generación, conservación y envío de facturas VERI*FACTU para la AEAT
(Agencia Española de Administración Tributaria).

Port of https://github.com/mdiago/VeriFactu (C#/.NET) to Python.
"""

__version__ = "1.0.68"

# ---------------- Negocio ----------------
from verifactu.business.invoice import Invoice
from verifactu.business.invoice_data import InvoiceData
from verifactu.business.tax_item import TaxItem
from verifactu.business.tax_class import TaxClass
from verifactu.business.rectification_item import RectificationItem
from verifactu.business.invoice_entry import InvoiceEntry
from verifactu.business.invoice_cancellation import InvoiceCancellation
from verifactu.business.invoice_fix import InvoiceFix
from verifactu.business.operations.invoice_action import InvoiceAction
from verifactu.business.operations.invoice_action_data import InvoiceActionData
from verifactu.business.operations.invoice_action_message import InvoiceActionMessage
from verifactu.business.operations.invoice_action_post import InvoiceActionPost

# ---------------- XML Factu ----------------
from verifactu.xml.namespaces import (
    NamespacePrefix, NamespaceSF, NamespaceSFLR, NamespaceTikR,
    NamespaceCon, NamespaceTikLRRC, NamespaceSf, NamespaceDs,
    NamespaceXades, NamespaceVNifV2Ent, NamespaceVNifV2Sal,
    NamespaceSoap, Items, EventItems, NifItems,
)
from verifactu.xml.xml_parser import XmlParser, XmlField
from verifactu.xml.factu.registro import Registro
from verifactu.xml.factu.registro_factura import RegistroFactura
from verifactu.xml.factu.reg_factu_sistema_facturacion import RegFactuSistemaFacturacion
from verifactu.xml.factu.id_factura import IDFactura
from verifactu.xml.factu.id_otro import IDOtro
from verifactu.xml.factu.interlocutor import Interlocutor
from verifactu.xml.factu.cabecera import Cabecera
from verifactu.xml.factu.encadenamiento import Encadenamiento
from verifactu.xml.factu.registro_anterior import RegistroAnterior
from verifactu.xml.factu.sistema_informatico import SistemaInformatico
from verifactu.xml.factu.remision_voluntaria import RemisionVoluntaria
from verifactu.xml.factu.remision_requerimiento import RemisionRequerimiento
from verifactu.xml.factu.datos_control import DatosControl
from verifactu.xml.factu.alta.registro_alta import RegistroAlta
from verifactu.xml.factu.alta.detalle_desglose import DetalleDesglose
from verifactu.xml.factu.alta.importe_rectificacion import ImporteRectificacion
from verifactu.xml.factu.anulacion.registro_anulacion import RegistroAnulacion
from verifactu.xml.factu.fault.fault import Fault
from verifactu.xml.factu.fault.detail import Detail
from verifactu.xml.factu.respuesta.respuesta_reg_factu_sistema_facturacion import (
    RespuestaRegFactuSistemaFacturacion)
from verifactu.xml.factu.respuesta.respuesta_linea import RespuestaLinea
from verifactu.xml.factu.respuesta.datos_presentacion import DatosPresentacion
from verifactu.xml.factu.respuesta.registro_duplicado import RegistroDuplicado

# ---------------- SOAP ----------------
from verifactu.xml.soap.envelope import Envelope
from verifactu.xml.soap.body import Body
from verifactu.xml.soap.header import Header

# ---------------- Enums ----------------
from verifactu.xml.factu.alta.tipo_factura import TipoFactura
from verifactu.xml.factu.alta.tipo_rectificativa import TipoRectificativa
from verifactu.xml.factu.alta.clave_regimen import ClaveRegimen
from verifactu.xml.factu.alta.calificacion_operacion import CalificacionOperacion
from verifactu.xml.factu.alta.causa_exencion import CausaExencion
from verifactu.xml.factu.alta.emitida_por_tercero_o_destinatario import (
    EmitidaPorTerceroODestinatario)
from verifactu.xml.factu.tipo_huella import TipoHuella
from verifactu.xml.factu.impuesto import Impuesto
from verifactu.xml.factu.id_type import IDType
from verifactu.xml.factu.codigo_pais import CodigoPais
from verifactu.xml.factu.rechazo_previo import RechazoPrevio

# ---------------- Configuración ----------------
from verifactu.config.settings import Settings
from verifactu.verifactu_environment import VeriFactuEnvironment
from verifactu.net.rest.api import Api

# ---------------- Cadena de bloques ----------------
from verifactu.blockchain.blockchain import Blockchain

# ---------------- Control de flujo ----------------
from verifactu.business.flow_control.invoice_queue import InvoiceQueue
from verifactu.business.flow_control.invoice_batch import InvoiceBatch, InvoicesBatch
from verifactu.business.flow_control.interval_worker import IntervalWorker
from verifactu.business.flow_control.seller_queue import SellerQueue

# ---------------- Eventos ----------------
from verifactu.business.events.events import EventData, EventEntry, EventFactory

# ---------------- Reenvío ----------------
from verifactu.business.invoice_retry_send import InvoiceRetrySend

# ---------------- Cadena de eventos ----------------
from verifactu.eventchain.event_chain import EventChain
from verifactu.eventchain.event_queue import EventQueue

# ---------------- QR ----------------
from verifactu.qrcode.qrcode_extensions import QRCode, QRCodeWriter, get_qr_bytes

# ---------------- Red ----------------
from verifactu.net.wsd import Wsd
from verifactu.net.rest.api_client import ApiClient

# ---------------- Utilidades ----------------
from verifactu.common.utils import Utils
from verifactu.common.logger import Logger
from verifactu.common.exceptions import (
    PostException, ClearPostException, SendException,
    UnexpectedHtmlException, FaultException, WriterException,
)

# ---------------- Validación ----------------
from verifactu.business.validation.nif.nif_validation import NifValidation
from verifactu.business.validation.nif.tax_id.tax_id_es import TaxIdEs
from verifactu.business.validation.nif.tax_id.tax_id_es_exception import TaxIdEsException
from verifactu.business.validation.nif.tax_id.enums import (
    TaxIdEsDCNif, TaxIdEsDCDniNie, TaxIdEsTypes, TaxIdEsError,
    TaxIdEsPersonTypeCode,
)
from verifactu.business.validation.vies.vies_vat_number import ViesVatNumber
from verifactu.business.validation.invoice_validation import InvoiceValidation
from verifactu.business.validation.validators.validator_cabecera import ValidatorCabecera
from verifactu.business.validation.validators.validator_sistema_informatico import (
    ValidatorSistemaInformatico)
from verifactu.business.validation.validators.validator_registro_factura import (
    ValidatorRegistroFactura)
from verifactu.business.validation.validators.alta.validator_registro_alta import (
    ValidatorRegistroAlta)
from verifactu.business.validation.validators.anulacion.validator_registro_anulacion import (
    ValidatorRegistroAnulacion)

# ---------------- Utilidades de fechas / importes ----------------
from verifactu.xml.xml_parser import (
    get_xml_date,
    get_xml_date_time_iso8601,
    get_xml_decimal,
    to_decimal,
    to_date,
    get_xml_enum_value,
    get_enum_from_xml_value,
)

__all__ = [
    # Negocio
    "Invoice", "InvoiceData", "TaxItem", "TaxClass", "RectificationItem",
    "InvoiceEntry", "InvoiceCancellation", "InvoiceFix",
    "InvoiceAction", "InvoiceActionData", "InvoiceActionMessage",
    "InvoiceActionPost",
    # XML
    "XmlParser", "XmlField", "Registro", "RegistroFactura",
    "RegFactuSistemaFacturacion", "IDFactura", "IDOtro", "Interlocutor",
    "Cabecera", "Encadenamiento", "RegistroAnterior", "SistemaInformatico",
    "RemisionVoluntaria", "RemisionRequerimiento", "DatosControl",
    "RegistroAlta", "DetalleDesglose", "ImporteRectificacion",
    "RegistroAnulacion", "Fault", "Detail",
    "RespuestaRegFactuSistemaFacturacion", "RespuestaLinea",
    "DatosPresentacion", "RegistroDuplicado",
    # SOAP
    "Envelope", "Body", "Header",
    # Enums
    "TipoFactura", "TipoRectificativa", "ClaveRegimen",
    "CalificacionOperacion", "CausaExencion",
    "EmitidaPorTerceroODestinatario", "TipoHuella", "Impuesto",
    "IDType", "CodigoPais", "RechazoPrevio",
    # Configuración
    "Settings", "VeriFactuEnvironment", "Api",
    # Blockchain / eventos
    "Blockchain", "EventChain", "EventQueue",
    # Control de flujo
    "InvoiceQueue", "InvoiceBatch", "InvoicesBatch",
    "IntervalWorker", "SellerQueue",
    "EventData", "EventEntry", "EventFactory",
    "InvoiceRetrySend",
    # QR
    "QRCode", "QRCodeWriter", "get_qr_bytes",
    # Red
    "Wsd", "ApiClient",
    # Utilidades
    "Utils", "Logger",
    "PostException", "ClearPostException", "SendException",
    "UnexpectedHtmlException", "FaultException", "WriterException",
    # Validación
    "NifValidation", "TaxIdEs", "TaxIdEsException",
    "TaxIdEsDCNif", "TaxIdEsDCDniNie", "TaxIdEsTypes", "TaxIdEsError",
    "TaxIdEsPersonTypeCode", "ViesVatNumber", "InvoiceValidation",
    "ValidatorCabecera", "ValidatorSistemaInformatico",
    "ValidatorRegistroFactura", "ValidatorRegistroAlta",
    "ValidatorRegistroAnulacion",
    # Fechas / importes
    "get_xml_date", "get_xml_date_time_iso8601", "get_xml_decimal",
    "to_decimal", "to_date", "get_xml_enum_value", "get_enum_from_xml_value",
    # Namespaces
    "NamespacePrefix", "NamespaceSF", "NamespaceSFLR", "NamespaceTikR",
    "NamespaceCon", "NamespaceTikLRRC", "NamespaceSf", "NamespaceDs",
    "NamespaceXades", "NamespaceVNifV2Ent", "NamespaceVNifV2Sal",
    "NamespaceSoap", "Items", "EventItems", "NifItems",
]
