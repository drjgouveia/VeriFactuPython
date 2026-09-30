"""SOAP Body."""

from verifactu.xml.xml_parser import XmlField
from verifactu.xml.namespaces import (
    NamespaceSoap, NamespaceSFLR, NamespaceTikR,
)


class Body:
    """SOAP body."""

    _XML_ROOT = ("Body", NamespaceSoap)

    def __init__(self, registro=None):
        self.registro = registro

    def _get_dynamic_fields(self):
        """El registro es polimórfico: el nombre y namespace dependen del tipo."""
        from verifactu.xml.factu.reg_factu_sistema_facturacion import (
            RegFactuSistemaFacturacion)
        from verifactu.xml.factu.respuesta.respuesta_reg_factu_sistema_facturacion import (
            RespuestaRegFactuSistemaFacturacion)
        from verifactu.xml.factu.fault.fault import Fault

        registro = self.registro
        if registro is None:
            return []
        if isinstance(registro, RegFactuSistemaFacturacion):
            return [XmlField("registro", name="RegFactuSistemaFacturacion",
                             ns=NamespaceSFLR)]
        if isinstance(registro, RespuestaRegFactuSistemaFacturacion):
            return [XmlField("registro", name="RespuestaRegFactuSistemaFacturacion",
                             ns=NamespaceTikR)]
        if isinstance(registro, Fault):
            return [XmlField("registro", name="Fault", ns=NamespaceSoap)]
        # Fallback: usa el nombre de la clase
        return [XmlField("registro", name=registro.__class__.__name__)]

    def __str__(self) -> str:
        return f"{self.registro}"
