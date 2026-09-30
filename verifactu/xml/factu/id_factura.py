"""IDFactura - Invoice identification data."""

from typing import Optional

from verifactu.xml.xml_parser import XmlField


class IDFactura:
    """Invoice identification data for VeriFactu."""

    _XML_FIELDS = [
        XmlField("id_emisor_factura", name="IDEmisorFactura"),
        XmlField("num_serie_factura", name="NumSerieFactura"),
        XmlField("fecha_expedicion_factura", name="FechaExpedicionFactura"),
        XmlField("id_emisor_factura_anulada", name="IDEmisorFacturaAnulada"),
        XmlField("num_serie_factura_anulada", name="NumSerieFacturaAnulada"),
        XmlField("fecha_expedicion_factura_anulada", name="FechaExpedicionFacturaAnulada"),
    ]

    def __init__(self):
        self._is_cancellation = False
        self._id_emisor = ""
        self._num_serie = ""
        self._fecha_expedicion = ""

    @property
    def id_emisor_factura(self) -> Optional[str]:
        return None if self._is_cancellation else self._id_emisor

    @id_emisor_factura.setter
    def id_emisor_factura(self, value: str):
        self._is_cancellation = False
        self._id_emisor = value

    @property
    def num_serie_factura(self) -> Optional[str]:
        return None if self._is_cancellation else self._num_serie

    @num_serie_factura.setter
    def num_serie_factura(self, value: str):
        self._is_cancellation = False
        self._num_serie = value

    @property
    def fecha_expedicion_factura(self) -> Optional[str]:
        return None if self._is_cancellation else self._fecha_expedicion

    @fecha_expedicion_factura.setter
    def fecha_expedicion_factura(self, value: str):
        self._is_cancellation = False
        self._fecha_expedicion = value

    @property
    def id_emisor_factura_anulada(self) -> Optional[str]:
        return self._id_emisor if self._is_cancellation else None

    @id_emisor_factura_anulada.setter
    def id_emisor_factura_anulada(self, value: str):
        self._is_cancellation = True
        self._id_emisor = value

    @property
    def num_serie_factura_anulada(self) -> Optional[str]:
        return self._num_serie if self._is_cancellation else None

    @num_serie_factura_anulada.setter
    def num_serie_factura_anulada(self, value: str):
        self._is_cancellation = True
        self._num_serie = value

    @property
    def fecha_expedicion_factura_anulada(self) -> Optional[str]:
        return self._fecha_expedicion if self._is_cancellation else None

    @fecha_expedicion_factura_anulada.setter
    def fecha_expedicion_factura_anulada(self, value: str):
        self._is_cancellation = True
        self._fecha_expedicion = value

    # Propiedades auxiliares internas (equivalente a las internal de C#)

    @property
    def id_emisor(self) -> Optional[str]:
        return self._id_emisor

    @id_emisor.setter
    def id_emisor(self, value: Optional[str]):
        self._id_emisor = value

    @property
    def num_serie(self) -> Optional[str]:
        return self._num_serie

    @num_serie.setter
    def num_serie(self, value: Optional[str]):
        self._num_serie = value

    @property
    def fecha_expedicion(self) -> Optional[str]:
        return self._fecha_expedicion

    @fecha_expedicion.setter
    def fecha_expedicion(self, value: Optional[str]):
        self._fecha_expedicion = value

    def __str__(self) -> str:
        return f"{self.id_emisor_factura}: {self.num_serie_factura} ({self.fecha_expedicion_factura})"