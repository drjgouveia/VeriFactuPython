"""Detail - Detalle del Fault SOAP."""

from verifactu.xml.xml_parser import XmlField


class Detail:
    """Detalle del Fault SOAP."""

    _XML_FIELDS = [
        XmlField("text", name="Text"),
    ]

    def __init__(self):
        self.text = None
