"""Respuesta a una presentación."""

from verifactu.xml.xml_parser import XmlField


class RespuestaRegFactuSistemaFacturacion:
    """Respuesta a una presentación."""

    _XML_ROOT = ("RespuestaRegFactuSistemaFacturacion", None)

    _XML_FIELDS = [
        XmlField("csv", name="CSV", order=1),
        XmlField("datos_presentacion", name="DatosPresentacion", order=2),
        XmlField("cabecera", name="Cabecera", order=3),
        XmlField("tiempo_espera_envio", name="TiempoEsperaEnvio", order=4),
        XmlField("estado_envio", name="EstadoEnvio", order=5),
        XmlField("respuesta_linea", name="RespuestaLinea", order=6,
                 is_array=True, array_item_name="RespuestaLinea"),
    ]

    def __init__(self):
        self.csv = None
        self.datos_presentacion = None
        self.cabecera = None
        self.tiempo_espera_envio = 0
        self.estado_envio = None
        self.respuesta_linea = []

    def __str__(self) -> str:
        return f"{self.estado_envio}-{self.csv}"
