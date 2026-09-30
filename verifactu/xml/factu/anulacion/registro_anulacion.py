"""RegistroAnulacion - Invoice cancellation record."""

from typing import Optional

from verifactu.xml.factu.registro import Registro
from verifactu.xml.factu.id_factura import IDFactura
from verifactu.xml.factu.sistema_informatico import SistemaInformatico
from verifactu.xml.factu.tipo_huella import TipoHuella
from verifactu.xml.xml_parser import XmlField
from verifactu.xml.namespaces import NamespaceSF, NamespaceSFLR


class RegistroAnulacion(Registro):
    """Registro de facturación de anulación."""

    _XML_ROOT = ("RegistroAnulacion", NamespaceSF)

    _XML_FIELDS = [
        XmlField("id_version", name="IDVersion", ns=NamespaceSF, order=1),
        XmlField("id_factura_anulada", name="IDFacturaAnulada", ns=NamespaceSF, order=2),
        XmlField("ref_externa", name="RefExterna", ns=NamespaceSF, order=3),
        XmlField("nombre_razon_emisor", name="NombreRazonEmisor", ns=NamespaceSF, order=4),
        XmlField("subsanacion", name="Subsanacion", order=5),
        XmlField("rechazo_previo", name="RechazoPrevio", order=6),
        XmlField("sistema_informatico", name="SistemaInformatico", ns=NamespaceSF, order=7),
        XmlField("ordered_fecha_hora_huso_gen_registro", name="FechaHoraHusoGenRegistro",
                 ns=NamespaceSF, order=8),
        XmlField("num_registro_acuerdo_facturacion", name="NumRegistroAcuerdoFacturacion",
                 ns=NamespaceSFLR, order=9),
        XmlField("id_acuerdo_sistema_informatico", name="IdAcuerdoSistemaInformatico",
                 ns=NamespaceSFLR, order=10),
        XmlField("tipo_huella", name="TipoHuella", ns=NamespaceSF, order=11, is_enum=True,
                 enum_type=TipoHuella, specified_attr="tipo_huella_specified"),
        XmlField("ordered_huella", name="Huella", ns=NamespaceSF, order=12),
    ]

    def __init__(self):
        super().__init__()
        self._id_factura_anulada: Optional[IDFactura] = None
        self._ref_externa: Optional[str] = None
        self._nombre_razon_emisor: str = ""
        self.subsanacion: Optional[str] = None
        self.rechazo_previo: Optional[str] = None
        self._sistema_informatico: Optional[SistemaInformatico] = None
        self._tipo_huella: TipoHuella = TipoHuella.Sha256
        self._tipo_huella_specified: bool = True
        self._num_registro_acuerdo_facturacion: Optional[str] = None
        self._id_acuerdo_sistema_informatico: Optional[str] = None
        self.ordered_fecha_hora_huso_gen_registro = None
        self.ordered_huella = None
        self.ordered_encadenamiento = None

    @property
    def id_factura_anulada(self) -> Optional[IDFactura]:
        return self._id_factura_anulada

    @id_factura_anulada.setter
    def id_factura_anulada(self, value: IDFactura):
        self._id_factura_anulada = value

    @property
    def nombre_razon_emisor(self) -> str:
        return self._nombre_razon_emisor

    @nombre_razon_emisor.setter
    def nombre_razon_emisor(self, value: str):
        self._nombre_razon_emisor = value

    @property
    def ref_externa(self) -> Optional[str]:
        return self._ref_externa

    @ref_externa.setter
    def ref_externa(self, value: Optional[str]):
        self._ref_externa = value

    @property
    def sistema_informatico(self) -> Optional[SistemaInformatico]:
        return self._sistema_informatico

    @sistema_informatico.setter
    def sistema_informatico(self, value: SistemaInformatico):
        self._sistema_informatico = value

    @property
    def encadenamiento(self):
        return self._encadenamiento

    @encadenamiento.setter
    def encadenamiento(self, value):
        self._encadenamiento = value
        self.ordered_encadenamiento = value

    @property
    def huella(self) -> str:
        return self._huella

    @huella.setter
    def huella(self, value: str):
        self._huella = value
        self.ordered_huella = value

    @property
    def fecha_hora_huso_gen_registro(self) -> str:
        return self._fecha_hora_huso_gen_registro

    @fecha_hora_huso_gen_registro.setter
    def fecha_hora_huso_gen_registro(self, value: str):
        self._fecha_hora_huso_gen_registro = value
        self.ordered_fecha_hora_huso_gen_registro = value

    def get_hash_text_input(self) -> str:
        # Artículo 137.b de la Orden HAC/1177/2024
        idf = self.id_factura_anulada
        return (f"IDEmisorFactura={idf.id_emisor if idf else ''}"
                f"&NumSerieFactura={idf.num_serie if idf else ''}"
                f"&FechaExpedicionFactura={idf.fecha_expedicion if idf else ''}"
                f"&Huella={self.encadenamiento.registro_anterior.huella if self.encadenamiento and self.encadenamiento.registro_anterior else ''}"
                f"&FechaHoraHusoGenRegistro={self.fecha_hora_huso_gen_registro}")

    def get_validate_url_params(self) -> str:
        from urllib.parse import quote
        idf = self.id_factura_anulada
        nif = quote(f"{idf.id_emisor if idf else ''}")
        numserie = quote(f"{idf.num_serie if idf else ''}")
        fecha = quote(f"{idf.fecha_expedicion if idf else ''}")
        importe = quote("0")
        return f"nif={nif}&numserie={numserie}&fecha={fecha}&importe={importe}"

    def set_extern_key(self):
        self.ref_externa = self.extern_key

    def __str__(self) -> str:
        return f"Anulacion-{self.id_factura_anulada}"
