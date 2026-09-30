"""ImporteRectificacion - Rectification amount data."""

from typing import Optional

from verifactu.xml.xml_parser import XmlField


class ImporteRectificacion:
    """Rectification amounts."""

    _XML_FIELDS = [
        XmlField("base_rectificada", name="BaseRectificada"),
        XmlField("cuota_rectificada", name="CuotaRectificada"),
        XmlField("cuota_recargo_rectificado", name="CuotaRecargoRectificado"),
    ]

    def __init__(self):
        self.base_rectificada: Optional[str] = None
        self.cuota_rectificada: Optional[str] = None
        self.cuota_recargo_rectificado: Optional[str] = None