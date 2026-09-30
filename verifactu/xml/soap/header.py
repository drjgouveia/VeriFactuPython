"""SOAP Header."""

from verifactu.xml.xml_parser import XmlField
from verifactu.xml.namespaces import NamespaceSoap


class Header:
    """SOAP Header."""

    _XML_ROOT = ("Header", NamespaceSoap)

    _XML_FIELDS = []
