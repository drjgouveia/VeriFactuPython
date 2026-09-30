"""RegistroAlta - Invoice registration record."""

from typing import Optional

from verifactu.xml.factu.registro import Registro
from verifactu.xml.factu.id_factura import IDFactura
from verifactu.xml.factu.encadenamiento import Encadenamiento
from verifactu.xml.factu.sistema_informatico import SistemaInformatico
from verifactu.xml.factu.tipo_huella import TipoHuella
from verifactu.xml.factu.alta.tipo_factura import TipoFactura
from verifactu.xml.factu.alta.tipo_rectificativa import TipoRectificativa
from verifactu.xml.factu.alta.clave_regimen import ClaveRegimen
from verifactu.xml.factu.alta.calificacion_operacion import CalificacionOperacion
from verifactu.xml.factu.interlocutor import Interlocutor
from verifactu.xml.factu.alta.detalle_desglose import DetalleDesglose
from verifactu.xml.factu.alta.emitida_por_tercero_o_destinatario import EmitidaPorTerceroODestinatario
from verifactu.xml.factu.rechazo_previo import RechazoPrevio
from verifactu.xml.xml_parser import XmlField
from verifactu.xml.namespaces import NamespaceSF, NamespaceSFLR, NamespaceDs


class RegistroAlta(Registro):
    """Registro de facturación de alta."""

    _XML_ROOT = ("RegistroAlta", NamespaceSF)

    _XML_FIELDS = [
        XmlField("id_version", name="IDVersion", ns=NamespaceSF, order=1),
        XmlField("id_factura_alta", name="IDFactura", ns=NamespaceSF, order=2),
        XmlField("ref_externa", name="RefExterna", ns=NamespaceSF, order=3),
        XmlField("nombre_razon_emisor", name="NombreRazonEmisor", ns=NamespaceSF, order=4),
        XmlField("subsanacion", name="Subsanacion", order=5),
        XmlField("rechazo_previo", name="RechazoPrevio", order=6, is_enum=True,
                 enum_type=RechazoPrevio, specified_attr="rechazo_previo_specified"),
        XmlField("tipo_factura", name="TipoFactura", ns=NamespaceSF, order=7, is_enum=True,
                 enum_type=TipoFactura),
        XmlField("tipo_rectificativa", name="TipoRectificativa", ns=NamespaceSF, order=8,
                 is_enum=True, enum_type=TipoRectificativa,
                 specified_attr="tipo_rectificativa_specified"),
        XmlField("facturas_rectificadas", name="FacturasRectificadas", ns=NamespaceSF, order=9,
                 is_array=True, array_item_name="IDFacturaRectificada",
                 array_item_ns=NamespaceSF),
        XmlField("facturas_sustituidas", name="FacturasSustituidas", ns=NamespaceSF, order=10,
                 is_array=True, array_item_name="IDFacturaSustituida",
                 array_item_ns=NamespaceSF),
        XmlField("importe_rectificacion", name="ImporteRectificacion", ns=NamespaceSF, order=11),
        XmlField("fecha_operacion", name="FechaOperacion", ns=NamespaceSF, order=12),
        XmlField("descripcion_operacion", name="DescripcionOperacion", ns=NamespaceSF, order=13),
        XmlField("factura_simplificada_art7273", name="FacturaSimplificadaArt7273", order=14),
        XmlField("factura_sin_identif_destinatario_art61d",
                 name="FacturaSinIdentifDestinatarioArt61d", order=15),
        XmlField("macrodato", name="Macrodato", ns=NamespaceSF, order=16),
        XmlField("emitida_por_tercero_o_destinatario", name="EmitidaPorTerceroODestinatario",
                 ns=NamespaceSF, order=17, is_enum=True,
                 enum_type=EmitidaPorTerceroODestinatario,
                 specified_attr="emitida_por_tercero_o_destinatario_specified"),
        XmlField("tercero", name="Tercero", ns=NamespaceSF, order=18),
        XmlField("destinatarios", name="Destinatarios", ns=NamespaceSF, order=19,
                 is_array=True, array_item_name="IDDestinatario",
                 array_item_ns=NamespaceSF),
        XmlField("cupon", name="Cupon", ns=NamespaceSF, order=20),
        XmlField("desglose", name="Desglose", ns=NamespaceSF, order=21,
                 is_array=True, array_item_name="DetalleDesglose",
                 array_item_ns=NamespaceSF),
        XmlField("cuota_total", name="CuotaTotal", ns=NamespaceSF, order=22),
        XmlField("importe_total", name="ImporteTotal", ns=NamespaceSF, order=23),
        XmlField("ordered_encadenamiento", name="Encadenamiento", ns=NamespaceSF, order=24),
        XmlField("sistema_informatico", name="SistemaInformatico", ns=NamespaceSF, order=25),
        XmlField("ordered_fecha_hora_huso_gen_registro", name="FechaHoraHusoGenRegistro",
                 ns=NamespaceSF, order=26),
        XmlField("num_registro_acuerdo_facturacion", name="NumRegistroAcuerdoFacturacion",
                 ns=NamespaceSFLR, order=27),
        XmlField("id_acuerdo_sistema_informatico", name="IdAcuerdoSistemaInformatico",
                 ns=NamespaceSFLR, order=28),
        XmlField("tipo_huella", name="TipoHuella", ns=NamespaceSF, order=29, is_enum=True,
                 enum_type=TipoHuella, specified_attr="tipo_huella_specified"),
        XmlField("ordered_huella", name="Huella", ns=NamespaceSF, order=30),
    ]

    def __init__(self):
        super().__init__()
        self._id_factura_alta: Optional[IDFactura] = None
        self._ref_externa: Optional[str] = None
        self._nombre_razon_emisor: str = ""
        self.subsanacion: Optional[str] = None
        self._rechazo_previo: Optional[RechazoPrevio] = None
        self._rechazo_previo_specified: bool = False
        self._tipo_factura: Optional[TipoFactura] = None
        self._tipo_rectificativa: Optional[TipoRectificativa] = None
        self._tipo_rectificativa_specified: bool = False
        self._facturas_rectificadas: list = []
        self._facturas_sustituidas: list = []
        self._importe_rectificacion = None
        self._fecha_operacion: Optional[str] = None
        self._descripcion_operacion: str = ""
        self._factura_simplificada_art7273: Optional[str] = None
        self._factura_sin_identif_destinatario_art61d: Optional[str] = None
        self._macrodato: Optional[str] = None
        self._emitida_por_tercero_o_destinatario: Optional[EmitidaPorTerceroODestinatario] = None
        self._emitida_por_tercero_o_destinatario_specified: bool = False
        self._tercero: Optional[Interlocutor] = None
        self._destinatarios: list = []
        self._cupon: Optional[str] = None
        self._desglose: list = []
        self._cuota_total: Optional[str] = None
        self._importe_total: Optional[str] = None
        self._sistema_informatico: Optional[SistemaInformatico] = None
        self._tipo_huella: TipoHuella = TipoHuella.Sha256
        self._tipo_huella_specified: bool = True
        self._num_registro_acuerdo_facturacion: Optional[str] = None
        self._id_acuerdo_sistema_informatico: Optional[str] = None
        self._signature = None
        self.ordered_encadenamiento = None
        self.ordered_fecha_hora_huso_gen_registro = None
        self.ordered_huella = None

    @property
    def id_factura_alta(self) -> Optional[IDFactura]:
        return self._id_factura_alta

    @id_factura_alta.setter
    def id_factura_alta(self, value: IDFactura):
        self._id_factura_alta = value

    @property
    def nombre_razon_emisor(self) -> str:
        return self._nombre_razon_emisor

    @nombre_razon_emisor.setter
    def nombre_razon_emisor(self, value: str):
        self._nombre_razon_emisor = value

    @property
    def tipo_factura(self) -> Optional[TipoFactura]:
        return self._tipo_factura

    @tipo_factura.setter
    def tipo_factura(self, value: TipoFactura):
        self._tipo_factura = value

    @property
    def tipo_rectificativa(self) -> Optional[TipoRectificativa]:
        return self._tipo_rectificativa

    @tipo_rectificativa.setter
    def tipo_rectificativa(self, value: TipoRectificativa):
        self._tipo_rectificativa = value

    @property
    def tipo_rectificativa_specified(self) -> bool:
        return self._tipo_rectificativa_specified

    @tipo_rectificativa_specified.setter
    def tipo_rectificativa_specified(self, value: bool):
        self._tipo_rectificativa_specified = value

    @property
    def facturas_rectificadas(self) -> list:
        return self._facturas_rectificadas

    @facturas_rectificadas.setter
    def facturas_rectificadas(self, value: list):
        self._facturas_rectificadas = value

    @property
    def facturas_sustituidas(self) -> list:
        return self._facturas_sustituidas

    @facturas_sustituidas.setter
    def facturas_sustituidas(self, value: list):
        self._facturas_sustituidas = value

    @property
    def importe_rectificacion(self) -> Optional[ImporteRectificacion]:
        return self._importe_rectificacion

    @importe_rectificacion.setter
    def importe_rectificacion(self, value: ImporteRectificacion):
        self._importe_rectificacion = value

    @property
    def fecha_operacion(self) -> Optional[str]:
        return self._fecha_operacion

    @fecha_operacion.setter
    def fecha_operacion(self, value: str):
        self._fecha_operacion = value

    @property
    def descripcion_operacion(self) -> str:
        return self._descripcion_operacion

    @descripcion_operacion.setter
    def descripcion_operacion(self, value: str):
        self._descripcion_operacion = value

    @property
    def desglose(self) -> list:
        return self._desglose

    @desglose.setter
    def desglose(self, value: list):
        self._desglose = value

    @property
    def cuota_total(self) -> Optional[str]:
        return self._cuota_total

    @cuota_total.setter
    def cuota_total(self, value: str):
        self._cuota_total = value

    @property
    def importe_total(self) -> Optional[str]:
        return self._importe_total

    @importe_total.setter
    def importe_total(self, value: str):
        self._importe_total = value

    @property
    def sistema_informatico(self) -> Optional[SistemaInformatico]:
        return self._sistema_informatico

    @sistema_informatico.setter
    def sistema_informatico(self, value: SistemaInformatico):
        self._sistema_informatico = value

    @property
    def rechazo_previo(self) -> Optional[RechazoPrevio]:
        return self._rechazo_previo

    @rechazo_previo.setter
    def rechazo_previo(self, value: RechazoPrevio):
        self._rechazo_previo = value

    @property
    def rechazo_previo_specified(self) -> bool:
        return self._rechazo_previo_specified

    @rechazo_previo_specified.setter
    def rechazo_previo_specified(self, value: bool):
        self._rechazo_previo_specified = value

    @property
    def destinatarios(self) -> list:
        return self._destinatarios

    @destinatarios.setter
    def destinatarios(self, value: list):
        self._destinatarios = value

    @property
    def tercero(self) -> Optional[Interlocutor]:
        return self._tercero

    @tercero.setter
    def tercero(self, value: Interlocutor):
        self._tercero = value

    @property
    def emitida_por_tercero_o_destinatario(self) -> Optional[EmitidaPorTerceroODestinatario]:
        return self._emitida_por_tercero_o_destinatario

    @emitida_por_tercero_o_destinatario.setter
    def emitida_por_tercero_o_destinatario(self, value: EmitidaPorTerceroODestinatario):
        self._emitida_por_tercero_o_destinatario = value

    @property
    def emitida_por_tercero_o_destinatario_specified(self) -> bool:
        return self._emitida_por_tercero_o_destinatario_specified

    @emitida_por_tercero_o_destinatario_specified.setter
    def emitida_por_tercero_o_destinatario_specified(self, value: bool):
        self._emitida_por_tercero_o_destinatario_specified = value

    @property
    def cupon(self) -> Optional[str]:
        return self._cupon

    @cupon.setter
    def cupon(self, value: str):
        self._cupon = value

    @property
    def factura_simplificada_art7273(self) -> Optional[str]:
        return self._factura_simplificada_art7273

    @factura_simplificada_art7273.setter
    def factura_simplificada_art7273(self, value: str):
        self._factura_simplificada_art7273 = value

    @property
    def factura_sin_identif_destinatario_art61d(self) -> Optional[str]:
        return self._factura_sin_identif_destinatario_art61d

    @factura_sin_identif_destinatario_art61d.setter
    def factura_sin_identif_destinatario_art61d(self, value: str):
        self._factura_sin_identif_destinatario_art61d = value

    @property
    def macrodato(self) -> Optional[str]:
        return self._macrodato

    @macrodato.setter
    def macrodato(self, value: str):
        self._macrodato = value

    @property
    def num_registro_acuerdo_facturacion(self) -> Optional[str]:
        return self._num_registro_acuerdo_facturacion

    @num_registro_acuerdo_facturacion.setter
    def num_registro_acuerdo_facturacion(self, value: str):
        self._num_registro_acuerdo_facturacion = value

    @property
    def id_acuerdo_sistema_informatico(self) -> Optional[str]:
        return self._id_acuerdo_sistema_informatico

    @id_acuerdo_sistema_informatico.setter
    def id_acuerdo_sistema_informatico(self, value: str):
        self._id_acuerdo_sistema_informatico = value

    @property
    def ref_externa(self) -> Optional[str]:
        return self._ref_externa

    @ref_externa.setter
    def ref_externa(self, value: Optional[str]):
        self._ref_externa = value

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
        self.id_factura = self.id_factura_alta
        return (f"IDEmisorFactura={self.id_factura_alta.id_emisor_factura if self.id_factura_alta else ''}"
                f"&NumSerieFactura={self.id_factura_alta.num_serie_factura if self.id_factura_alta else ''}"
                f"&FechaExpedicionFactura={self.id_factura_alta.fecha_expedicion_factura if self.id_factura_alta else ''}"
                f"&TipoFactura={self.tipo_factura.value if self.tipo_factura else ''}"
                f"&CuotaTotal={self.cuota_total}"
                f"&ImporteTotal={self.importe_total}"
                f"&Huella={self.encadenamiento.registro_anterior.huella if self.encadenamiento and self.encadenamiento.registro_anterior else ''}"
                f"&FechaHoraHusoGenRegistro={self.fecha_hora_huso_gen_registro}")

    def get_validate_url_params(self) -> str:
        from urllib.parse import quote
        nif = quote(f"{self.id_factura_alta.id_emisor_factura if self.id_factura_alta else ''}")
        numserie = quote(f"{self.id_factura_alta.num_serie_factura if self.id_factura_alta else ''}")
        fecha = quote(f"{self.id_factura_alta.fecha_expedicion_factura if self.id_factura_alta else ''}")
        importe = quote(f"{self.importe_total}")
        return f"nif={nif}&numserie={numserie}&fecha={fecha}&importe={importe}"

    def set_extern_key(self):
        self.ref_externa = self.extern_key

    def __str__(self) -> str:
        return f"{self.tipo_factura}-{self.id_factura_alta}"