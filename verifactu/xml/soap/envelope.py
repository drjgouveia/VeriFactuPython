"""SOAP Envelope."""

from verifactu.xml.xml_parser import XmlField, XmlParser
from verifactu.xml.soap.header import Header
from verifactu.xml.soap.body import Body
from verifactu.xml.namespaces import NamespaceSoap, Items


class Envelope:
    """Representación de envelope (sobre) para SOAP."""

    _XML_ROOT = ("Envelope", NamespaceSoap)

    _XML_FIELDS = [
        XmlField("header", name="Header", ns=NamespaceSoap, order=1),
        XmlField("body", name="Body", ns=NamespaceSoap, order=2),
    ]

    def __init__(self, xml_path=None):
        self.header = Header()
        self.body = Body()
        if xml_path:
            with open(xml_path, "r", encoding="utf-8") as f:
                xml_content = f.read()
            envelope = Envelope.from_xml(xml_content)
            self.header = envelope.header
            self.body = envelope.body

    @staticmethod
    def from_xml(xml: str) -> "Envelope":
        """Devuelve un objeto envelope a partir de un string xml."""
        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml)

        envelope = Envelope()
        ns = NamespaceSoap
        header_elem = root.find(f"{{{ns}}}Header")
        if header_elem is not None:
            envelope.header = Header()

        body_elem = root.find(f"{{{ns}}}Body")
        if body_elem is not None:
            envelope.body = Body()
            for child in body_elem:
                local_name = child.tag.split('}')[-1]
                registro = _parse_body_registro(local_name, child)
                envelope.body.registro = registro
        return envelope

    def __str__(self) -> str:
        return f"{self.body}"


def _parse_body_registro(local_name, child):
    """Detecta y deserializa el registro del body SOAP."""
    text = child if child is None else child

    if local_name == "Fault":
        from verifactu.xml.factu.fault.fault import Fault
        fault = Fault()
        for sub in child:
            sub_name = sub.tag.split('}')[-1]
            if sub_name == "faultcode":
                fault.faultcode = sub.text
            elif sub_name == "faultstring":
                fault.faultstring = sub.text
            elif sub_name == "detail":
                fault.detail = _parse_fault_detail(sub)
        return fault

    if local_name == "RespuestaRegFactuSistemaFacturacion":
        from verifactu.xml.factu.respuesta.respuesta_reg_factu_sistema_facturacion import (
            RespuestaRegFactuSistemaFacturacion)
        return _deserialize(child, RespuestaRegFactuSistemaFacturacion())

    if local_name == "RegFactuSistemaFacturacion":
        from verifactu.xml.factu.reg_factu_sistema_facturacion import (
            RegFactuSistemaFacturacion)
        return _deserialize(child, RegFactuSistemaFacturacion())

    # Por defecto, devuelve el xml como texto
    import xml.etree.ElementTree as ET
    return ET.tostring(child, encoding='unicode')


def _parse_fault_detail(elem):
    from verifactu.xml.factu.fault.detail import Detail
    detail = Detail()
    for sub in elem:
        detail.text = (detail.text or "") + (sub.text or "")
    return detail


def _deserialize(elem, obj):
    """Deserialización genérica simple: mapea hijos a atributos snake_case."""
    import xml.etree.ElementTree as ET
    from verifactu.xml.xml_parser import XmlField

    def to_snake(name):
        import re
        s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    for child in elem:
        local_name = child.tag.split('}')[-1]
        attr = to_snake(local_name)
        if len(child) > 0:
            # Elemento complejo: delegamos a un sub-objeto dict-like simple
            setattr(obj, attr, _complex_to_value(child))
        else:
            setattr(obj, attr, child.text)
    return obj


def _complex_to_value(elem):
    """Convierte un elemento complejo en una estructura simple."""
    result = {}
    for child in elem:
        local_name = child.tag.split('}')[-1]
        if len(child) > 0:
            key = local_name
            values = result.setdefault(key, [])
            values.append(_complex_to_value(child))
        else:
            result[local_name] = child.text
    return result
