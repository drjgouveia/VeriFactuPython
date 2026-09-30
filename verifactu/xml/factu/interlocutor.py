"""Interlocutor - Counterparty data."""

from typing import Optional

from verifactu.xml.xml_parser import XmlField


class Interlocutor:
    """Interlocutor / counter-party data."""

    _XML_FIELDS = [
        XmlField("nombre_razon", name="NombreRazon"),
        XmlField("nif", name="NIF"),
        XmlField("id_otro", name="IDOtro"),
    ]

    def __init__(self):
        self.nombre_razon: Optional[str] = None
        self.nif: Optional[str] = None
        self.id_otro: Optional['IDOtro'] = None

    def __str__(self) -> str:
        return f"{self.nombre_razon} ({self.nif})"