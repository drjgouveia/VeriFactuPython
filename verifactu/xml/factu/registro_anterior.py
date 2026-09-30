"""RegistroAnterior - Previous record data."""

from typing import Optional

from verifactu.xml.xml_parser import XmlField


class RegistroAnterior:
    """Datos del registro anterior en la cadena."""

    _XML_FIELDS = [
        XmlField("id_emisor_factura", name="IDEmisorFactura"),
        XmlField("num_serie_factura", name="NumSerieFactura"),
        XmlField("fecha_expedicion_factura", name="FechaExpedicionFactura"),
        XmlField("huella", name="Huella"),
    ]

    def __init__(self):
        self.huella: Optional[str] = None
        self.fecha_expedicion_factura: Optional[str] = None
        self.id_emisor_factura: Optional[str] = None
        self.num_serie_factura: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.huella}"