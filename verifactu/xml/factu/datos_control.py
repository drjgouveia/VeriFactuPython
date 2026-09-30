"""DatosControl - Datos de control."""

from verifactu.xml.xml_parser import XmlField


class DatosControl:
    """Datos de control del envío (afectados por ISS)."""

    _XML_FIELDS = [
        XmlField("afectados_iss", name="AfectadosISS", is_array=True,
                 array_item_name="AfectadoISS"),
    ]

    def __init__(self):
        self.afectados_iss = []
