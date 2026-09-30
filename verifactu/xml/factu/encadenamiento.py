"""Encadenamiento - Blockchain linkage data."""

from typing import Optional

from verifactu.xml.xml_parser import XmlField
from verifactu.xml.factu.registro_anterior import RegistroAnterior


class Encadenamiento:
    """Encadenamiento con la factura anterior."""

    _XML_FIELDS = [
        XmlField("primer_registro", name="PrimerRegistro"),
        XmlField("registro_anterior", name="RegistroAnterior"),
    ]

    def __init__(self):
        self.primer_registro: Optional[str] = None
        self.registro_anterior: Optional['RegistroAnterior'] = None

    def __str__(self) -> str:
        return f"{self.registro_anterior}"