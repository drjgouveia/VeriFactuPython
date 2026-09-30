"""IDOtro - Alternative identification data."""

from typing import Optional

from verifactu.xml.xml_parser import XmlField
from verifactu.xml.factu.id_type import IDType
from verifactu.xml.factu.codigo_pais import CodigoPais
from verifactu.xml.factu.id_type import IDType


class IDOtro:
    """Alternative identification."""

    _XML_FIELDS = [
        XmlField("codigo_pais", name="CodigoPais", is_enum=True, enum_type=CodigoPais),
        XmlField("id_type", name="IDType", is_enum=True, enum_type=IDType),
        XmlField("id", name="ID"),
    ]

    def __init__(self):
        self.id: Optional[str] = None
        self.id_type: Optional[IDType] = None
        self.codigo_pais: Optional[CodigoPais] = None
        self.codigo_pais_specified: bool = False