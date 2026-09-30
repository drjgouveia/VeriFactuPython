"""RespuestaLinea - Línea de respuesta."""

from verifactu.xml.xml_parser import XmlField


class RespuestaLinea:
    """Línea de respuesta del envío."""

    _XML_FIELDS = [
        XmlField("id_factura", name="IDFactura", order=1),
        XmlField("operacion", name="Operacion", order=2),
        XmlField("estado_registro", name="EstadoRegistro", order=3),
        XmlField("descripcion_error_registro", name="DescripcionErrorRegistro", order=4),
        XmlField("codigo_error_registro", name="CodigoErrorRegistro", order=5),
        XmlField("registro_duplicado", name="RegistroDuplicado", order=6),
    ]

    def __init__(self):
        self.id_factura = None
        self.operacion = None
        self.estado_registro = None
        self.descripcion_error_registro = None
        self.codigo_error_registro = None
        self.registro_duplicado = None

    def __str__(self) -> str:
        return f"{self.id_factura}: {self.estado_registro}"
