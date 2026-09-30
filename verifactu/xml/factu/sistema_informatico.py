"""SistemaInformatico - Información del sistema informático."""

from typing import Optional

from verifactu.xml.xml_parser import XmlField
from verifactu.xml.factu.id_otro import IDOtro


class SistemaInformatico:
    """Información del sistema informático de facturación."""

    _XML_FIELDS = [
        XmlField("nif", name="NIF"),
        XmlField("ido_otro", name="IDOtro"),
        XmlField("nombre_razon", name="NombreRazon"),
        XmlField("nombre_razon_representante", name="NombreRazonRepresentante"),
        XmlField("nif_representante", name="NIFRepresentante"),
        XmlField("nombre_sistema_informatico", name="NombreSistemaInformatico"),
        XmlField("id_sistema_informatico", name="IdSistemaInformatico"),
        XmlField("version", name="Version"),
        XmlField("numero_instalacion", name="NumeroInstalacion"),
        XmlField("tipo_uso_posible_solo_verifactu", name="TipoUsoPosibleSoloVerifactu"),
        XmlField("tipo_uso_posible_multi_ot", name="TipoUsoPosibleMultiOT"),
        XmlField("indicador_multiples_ot", name="IndicadorMultiplesOT"),
    ]

    def __init__(self):
        self.nif: str = ""
        self.ido_otro: Optional[IDOtro] = None
        self.nombre_razon: str = ""
        self.nombre_razon_representante: Optional[str] = None
        self.nif_representante: Optional[str] = None
        self.nombre_sistema_informatico: str = ""
        self.id_sistema_informatico: str = ""
        self.version: str = ""
        self.numero_instalacion: str = ""
        self.tipo_uso_posible_solo_verifactu: str = "N"
        self.tipo_uso_posible_multi_ot: str = "S"
        self.indicador_multiples_ot: str = "S"

    def __str__(self) -> str:
        return f"{self.nombre_razon} ({self.nif})"
