"""Serializador xml para VERI*FACTU.

Provides a reflective XML serializer/deserializer for the VeriFactu
data classes. Classes declare their XML mapping metadata in the class
attribute ``_XML_FIELDS`` (a list of :class:`XmlField`) and optionally
the root element in ``_XML_ROOT`` (a ``(name, namespace)`` tuple).
"""

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field as dc_field
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, Type, TypeVar

from verifactu.xml.namespaces import NamespaceSoap

T = TypeVar('T')


def _utils():
    """Import lazy para evitar dependencia circular."""
    from verifactu.common.utils import Utils
    return Utils


@dataclass
class XmlField:
    """Metadatos de serialización XML de una propiedad."""
    attr: str
    name: str = None
    ns: str = None
    order: int = 0
    is_array: bool = False
    is_flat: bool = False
    array_item_name: str = None
    array_item_ns: str = None
    is_enum: bool = False
    enum_type: Type = None
    specified_attr: str = None


def _value_to_text(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Decimal):
        return str(value)
    return str(value)


def _qualify(ns: Optional[str], name: str, nsmap: Dict[str, str]) -> str:
    if not ns:
        return name
    for prefix, uri in nsmap.items():
        if uri == ns:
            return f"{prefix}:{name}" if prefix else name
    return name


def _serialize_element(obj: Any, parent: ET.Element, meta: List[XmlField],
                       nsmap: Dict[str, str], default_ns: Optional[str] = None):
    if meta is None and hasattr(obj, '_get_dynamic_fields'):
        meta = obj._get_dynamic_fields()
    fields = sorted(meta, key=lambda f: f.order)
    for f in fields:
        value = getattr(obj, f.attr, None)
        if value is None:
            continue
        if f.specified_attr is not None and not getattr(obj, f.specified_attr, False):
            continue
        ns = f.ns or default_ns
        if f.is_array:
            if not isinstance(value, (list, tuple)) or len(value) == 0:
                continue
            if f.is_flat:
                # Array plano: los elementos se repiten sin wrapper
                item_name = _qualify(f.array_item_ns or ns,
                                     f.array_item_name or f.name or f.attr, nsmap)
                for item in value:
                    if item is None:
                        continue
                    item_elem = ET.SubElement(parent, item_name)
                    _serialize_item(item, item_elem, nsmap, f.array_item_ns or ns)
            else:
                array_name = _qualify(ns, f.name or f.attr, nsmap)
                array_elem = ET.SubElement(parent, array_name)
                item_name = _qualify(f.array_item_ns or ns,
                                     f.array_item_name or "Item", nsmap)
                for item in value:
                    if item is None:
                        continue
                    item_elem = ET.SubElement(array_elem, item_name)
                    _serialize_item(item, item_elem, nsmap, f.array_item_ns or ns)
        else:
            elem_name = _qualify(ns, f.name or f.attr, nsmap)
            elem = ET.SubElement(parent, elem_name)
            if isinstance(value, (str, int, float, Decimal, bool)):
                elem.text = _value_to_text(value)
            elif hasattr(value, '_XML_FIELDS'):
                _serialize_object(value, elem, value._XML_FIELDS, nsmap, ns)
            elif hasattr(value, '_get_dynamic_fields'):
                _serialize_object(value, elem, None, nsmap, ns)
            else:
                # Enum: usa el valor de serialización XML definido
                utils = _utils()
                elem.text = utils.get_xml_enum_value(value)


def _serialize_item(item, item_elem: ET.Element, nsmap: Dict[str, str],
                    default_ns: Optional[str]):
    """Serializa un elemento de una colección."""
    if hasattr(item, '_XML_FIELDS'):
        _serialize_object(item, item_elem, item._XML_FIELDS, nsmap, default_ns)
    elif hasattr(item, '_get_dynamic_fields'):
        _serialize_object(item, item_elem, None, nsmap, default_ns)
    else:
        item_elem.text = _value_to_text(item)


def _serialize_object(obj: Any, elem: ET.Element, meta: List[XmlField],
                      nsmap: Dict[str, str], default_ns: Optional[str] = None):
    _serialize_element(obj, elem, meta, nsmap, default_ns)


def _deserialize_element(obj: Any, elem: ET.Element, meta: List[XmlField]):
    meta_by_name = {f.name or f.attr: f for f in meta}
    arrays = [f for f in meta if f.is_array]
    for child in elem:
        local_name = child.tag.split('}')[-1]
        f = meta_by_name.get(local_name)
        if f is None:
            continue
        if f.is_array:
            items = getattr(obj, f.attr, None)
            if items is None:
                items = []
                setattr(obj, f.attr, items)
            for item_elem in child:
                item_cls = _detect_item_class(item_elem)
                item = item_cls()
                if hasattr(item, '_XML_FIELDS'):
                    _deserialize_element(item, item_elem, item._XML_FIELDS)
                else:
                    item = item_elem.text
                items.append(item)
        else:
            text = child.text
            value = text
            if f.is_enum and text and f.enum_type is not None:
                value = _utils().get_enum_from_xml_value(f.enum_type, text)
            setattr(obj, f.attr, value)


def _detect_item_class(item_elem: ET.Element) -> Type:
    from verifactu.xml.factu.interlocutor import Interlocutor
    from verifactu.xml.factu.id_factura import IDFactura
    from verifactu.xml.factu.alta.detalle_desglose import DetalleDesglose
    local_name = item_elem.tag.split('}')[-1]
    return {
        "IDDestinatario": Interlocutor,
        "DetalleDesglose": DetalleDesglose,
        "IDFacturaRectificada": IDFactura,
        "IDFacturaSustituida": IDFactura,
    }.get(local_name, Interlocutor)


class XmlParser:
    """Serializador xml."""

    def __init__(self):
        self.encoding = "UTF-8"

    def get_bytes(self, instance: Any, namespaces: Dict[str, str],
                  indent: bool = False, omit_xml_declaration: bool = True) -> bytes:
        root_name, root_ns = getattr(instance, '_XML_ROOT', (instance.__class__.__name__, None))
        nsmap = dict(namespaces or {})
        root = ET.Element(_qualify(root_ns, root_name, nsmap))
        _serialize_object(instance, root, getattr(instance, "_XML_FIELDS", []), nsmap, root_ns)
        if not omit_xml_declaration:
            xml_bytes = ET.tostring(root, encoding='unicode', xml_declaration=True)
        else:
            xml_bytes = ET.tostring(root, encoding='unicode')
        return xml_bytes.encode(self.encoding)

    def get_string(self, instance: Any, namespaces: Dict[str, str],
                   indent: bool = False, omit_xml_declaration: bool = True) -> str:
        return self.get_bytes(instance, namespaces, indent, omit_xml_declaration).decode(self.encoding)

    def get_instance(self, xml: str, cls: Type[T]) -> T:
        """Obtiene una instancia de un tipo a partir de un string xml."""
        root = ET.fromstring(xml)
        instance = cls()
        meta = getattr(cls, '_XML_FIELDS', [])
        if meta:
            _deserialize_element(instance, root, meta)
        return instance


# ---------------------------- utilidades ----------------------------

def get_xml_date(date: Optional[datetime] = None) -> str:
    """Devuelve una fecha formateada para un campo Fecha de VeriFactu (dd-MM-yyyy)."""
    if date is None:
        date = datetime(1, 1, 1)
    return date.strftime("%d-%m-%Y")


def get_xml_date_time_iso8601(date: Optional[datetime] = None) -> str:
    """Devuelve una fecha formateada para un campo FechaHoraHuso (ISO 8601)."""
    if date is None:
        date = datetime(1, 1, 1)
    return date.isoformat(timespec='seconds')


def get_xml_decimal(amount: Optional[Decimal]) -> Optional[str]:
    """Devuelve un importe formateado para un campo decimal de VeriFactu."""
    if amount is None:
        return None
    return f"{amount:g}" if isinstance(amount, float) else str(amount)


def to_decimal(amount: Optional[str]) -> Decimal:
    """Devuelve un decimal a partir de un string xml."""
    if amount is None or amount == "":
        return Decimal("0")
    return Decimal(amount.replace(",", "."))


def to_date(date_str: Optional[str]) -> datetime:
    """Devuelve una fecha a partir de un string xml (dd-MM-yyyy)."""
    if not date_str:
        return datetime(1, 1, 1)
    return datetime.strptime(date_str, "%d-%m-%Y")


def get_xml_enum_value(value) -> Optional[str]:
    """Obtiene el valor XML asociado a un valor enumerado."""
    if value is None:
        return None
    return _utils().get_xml_enum_value(value)


def get_enum_from_xml_value(enum_type: Type[T], value: str) -> T:
    """Obtiene un valor enumerado a partir de su valor XML."""
    return _utils().get_enum_from_xml_value(enum_type, value)


def serialize_xml(obj: Any, namespaces: Dict[str, str], indent: bool = False,
                  omit_xml_declaration: bool = True) -> str:
    """Serializa el objeto como xml y lo devuelve como cadena."""
    return XmlParser().get_string(obj, namespaces, indent, omit_xml_declaration)


def get_instance(xml_str: str, cls: Type[T]) -> T:
    """Deserializa un objeto a partir de un string xml."""
    return XmlParser().get_instance(xml_str, cls)
