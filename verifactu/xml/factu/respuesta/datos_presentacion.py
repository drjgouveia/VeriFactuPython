"""DatosPresentacion - Datos de la presentación."""

from verifactu.xml.xml_parser import XmlField


class DatosPresentacion:
    """Datos de la presentación a la que se refiere la respuesta."""

    _XML_FIELDS = [
        XmlField("nif_presentador", name="NIFPresentador"),
        XmlField("timestamp_presentacion", name="TimestampPresentacion"),
    ]

    def __init__(self):
        self.nif_presentador = None
        self.timestamp_presentacion = None
