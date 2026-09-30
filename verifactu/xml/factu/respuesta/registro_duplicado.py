"""RegistroDuplicado - Datos de un registro duplicado."""

from verifactu.xml.xml_parser import XmlField


class RegistroDuplicado:
    """Datos de la versión ya registrada de la factura."""

    _XML_FIELDS = [
        XmlField("id_version", name="IDVersion"),
        XmlField("id_emisor_factura", name="IDEmisorFactura"),
        XmlField("num_serie_factura", name="NumSerieFactura"),
        XmlField("fecha_expedicion_factura", name="FechaExpedicionFactura"),
        XmlField("estado_registro_duplicado", name="EstadoRegistroDuplicado"),
        XmlField("csv_duplicado", name="CSVDuplicado"),
        XmlField("fecha_hora_huso_gen_registro_duplicado",
                 name="FechaHoraHusoGenRegistroDuplicado"),
    ]

    def __init__(self):
        self.id_version = None
        self.id_emisor_factura = None
        self.num_serie_factura = None
        self.fecha_expedicion_factura = None
        self.estado_registro_duplicado = None
        self.csv_duplicado = None
        self.fecha_hora_huso_gen_registro_duplicado = None
