"""Cabecera - Invoice header data."""

from typing import Optional

from verifactu.xml.xml_parser import XmlField
from verifactu.xml.factu.interlocutor import Interlocutor
from verifactu.xml.factu.remision_voluntaria import RemisionVoluntaria
from verifactu.xml.factu.remision_requerimiento import RemisionRequerimiento
from verifactu.xml.namespaces import NamespaceSF, NamespaceSFLR


class Cabecera:
    """Datos de contexto de un suministro."""

    _XML_ROOT = ("Cabecera", NamespaceSF)

    _XML_FIELDS = [
        XmlField("obligado_emision", name="ObligadoEmision", ns=NamespaceSF),
        XmlField("representante", name="Representante", ns=NamespaceSF),
        XmlField("remision_voluntaria", name="RemisionVoluntaria", ns=NamespaceSF),
        XmlField("remision_requerimiento", name="RemisionRequerimiento", ns=NamespaceSF),
    ]

    def __init__(self):
        self.obligado_emision: Optional[Interlocutor] = None
        self.representante: Optional[Interlocutor] = None
        self.remision_voluntaria: Optional[RemisionVoluntaria] = None
        self.remision_requerimiento: Optional[RemisionRequerimiento] = None

    def __str__(self) -> str:
        return f"{self.obligado_emision}"