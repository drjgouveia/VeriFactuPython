"""Fault - SOAP Fault."""

from verifactu.xml.xml_parser import XmlField


class Fault:
    """SOAP Fault."""

    _XML_ROOT = ("Fault", None)

    _XML_FIELDS = [
        XmlField("faultcode", name="faultcode", order=1),
        XmlField("faultstring", name="faultstring", order=2),
        XmlField("detail", name="detail", order=3),
    ]

    def __init__(self):
        self.faultcode = None
        self.faultstring = None
        self.detail = None

    def __str__(self) -> str:
        return f"{self.faultcode}: {self.faultstring}"
