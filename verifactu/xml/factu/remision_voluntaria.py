"""RemisionVoluntaria - Datos referentes a la remisión voluntaria."""

from typing import Optional

from verifactu.xml.xml_parser import XmlField


class RemisionVoluntaria:
    """Datos referentes a la remisión voluntaria."""

    _XML_FIELDS = [
        XmlField("fecha_fin_veri_factu", name="FechaFinVeriFactu"),
        XmlField("incidencia", name="Incidencia"),
    ]

    def __init__(self):
        self.fecha_fin_veri_factu: Optional[str] = None
        self.incidencia: Optional[str] = None
