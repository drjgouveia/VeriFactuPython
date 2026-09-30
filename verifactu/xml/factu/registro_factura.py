"""RegistroFactura - Registro de alta o de anulación."""

from verifactu.xml.xml_parser import XmlField
from verifactu.xml.namespaces import NamespaceSF


class RegistroFactura:
    """Representa un registro de alta o de anulación."""

    def __init__(self):
        self.registro = None

    def _get_dynamic_fields(self):
        """El registro es polimórfico: RegistroAlta o RegistroAnulacion."""
        from verifactu.xml.factu.alta.registro_alta import RegistroAlta
        from verifactu.xml.factu.anulacion.registro_anulacion import RegistroAnulacion

        registro = self.registro
        if isinstance(registro, RegistroAlta):
            return [XmlField("registro", name="RegistroAlta", ns=NamespaceSF)]
        if isinstance(registro, RegistroAnulacion):
            return [XmlField("registro", name="RegistroAnulacion", ns=NamespaceSF)]
        return []

    def __str__(self) -> str:
        return f"{self.registro}"
