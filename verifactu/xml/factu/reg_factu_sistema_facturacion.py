"""Registro de envío de alta o anulación al sistema de facturación."""

from typing import List

from verifactu.xml.xml_parser import XmlField
from verifactu.xml.factu.cabecera import Cabecera
from verifactu.xml.factu.datos_control import DatosControl
from verifactu.xml.namespaces import NamespaceSFLR, NamespaceSF


class RegFactuSistemaFacturacion:
    """Registro de envío de alta o anulación al sistema de facturación."""

    _XML_ROOT = ("RegFactuSistemaFacturacion", NamespaceSFLR)

    _XML_FIELDS = [
        XmlField("cabecera", name="Cabecera", ns=NamespaceSFLR, order=1),
        XmlField("registro_factura", name="RegistroFactura", ns=NamespaceSFLR, order=2,
                 is_array=True, is_flat=True, array_item_name="RegistroFactura",
                 array_item_ns=NamespaceSFLR),
        XmlField("datos_control", name="DatosControl", ns=NamespaceSFLR, order=3),
    ]

    def __init__(self):
        self.cabecera = None
        self.registro_factura: List = []
        self.datos_control = None

    def __str__(self) -> str:
        return f"Envío: {self.cabecera} ({len(self.registro_factura or [])})"
