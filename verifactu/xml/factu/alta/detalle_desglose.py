"""DetalleDesglose - Invoice tax breakdown line."""

from typing import Optional

from verifactu.xml.xml_parser import XmlField
from verifactu.xml.factu.impuesto import Impuesto
from verifactu.xml.factu.alta.clave_regimen import ClaveRegimen
from verifactu.xml.factu.alta.calificacion_operacion import CalificacionOperacion
from verifactu.xml.factu.alta.causa_exencion import CausaExencion


class DetalleDesglose:
    """Linea de desglose de la factura."""

    _XML_FIELDS = [
        XmlField("impuesto", name="Impuesto", is_enum=True, enum_type=Impuesto),
        XmlField("clave_regimen", name="ClaveRegimen", is_enum=True, enum_type=ClaveRegimen,
                 specified_attr="clave_regimen_specified"),
        XmlField("calificacion_operacion", name="CalificacionOperacion", is_enum=True,
                 enum_type=CalificacionOperacion, specified_attr="calificacion_operacion_specified"),
        XmlField("operacion_exenta", name="OperacionExenta", is_enum=True, enum_type=CausaExencion,
                 specified_attr="operacion_exenta_specified"),
        XmlField("tipo_impositivo", name="TipoImpositivo"),
        XmlField("base_imponible_o_importe_no_sujeto", name="BaseImponibleOimporteNoSujeto"),
        XmlField("base_imponible_a_coste", name="BaseImponibleACoste"),
        XmlField("cuota_repercutida", name="CuotaRepercutida"),
        XmlField("tipo_recargo_equivalencia", name="TipoRecargoEquivalencia"),
        XmlField("cuota_recargo_equivalencia", name="CuotaRecargoEquivalencia"),
    ]

    def __init__(self):
        self.impuesto: Impuesto = Impuesto.IVA
        self.clave_regimen: ClaveRegimen = ClaveRegimen.RegimenGeneral
        self.clave_regimen_specified: bool = True
        self.calificacion_operacion: Optional[CalificacionOperacion] = None
        self.calificacion_operacion_specified: bool = False
        self.operacion_exenta: Optional[CausaExencion] = None
        self.operacion_exenta_specified: bool = False
        self.tipo_impositivo: Optional[str] = None
        self.base_imponible_o_importe_no_sujeto: Optional[str] = None
        self.base_imponible_a_coste: Optional[str] = None
        self.cuota_repercutida: Optional[str] = None
        self.tipo_recargo_equivalencia: Optional[str] = None
        self.cuota_recargo_equivalencia: Optional[str] = None

    def __str__(self) -> str:
        return (f"[{self.clave_regimen}, {self.calificacion_operacion}] "
                f"{self.base_imponible_o_importe_no_sujeto} x {self.tipo_impositivo} "
                f"= {self.cuota_repercutida}")