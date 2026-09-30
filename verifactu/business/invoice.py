"""Invoice - Main invoice class."""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from verifactu.xml.factu.alta.registro_alta import RegistroAlta
from verifactu.xml.factu.anulacion.registro_anulacion import RegistroAnulacion
from verifactu.xml.factu.alta.tipo_factura import TipoFactura
from verifactu.xml.factu.alta.tipo_rectificativa import TipoRectificativa
from verifactu.xml.factu.id_factura import IDFactura
from verifactu.business.invoice_data import InvoiceData
from verifactu.business.tax_item import TaxItem
from verifactu.business.tax_class import TaxClass
from verifactu.xml.factu.tipo_huella import TipoHuella
from verifactu.xml.factu.alta.importe_rectificacion import ImporteRectificacion
from verifactu.xml.factu.alta.detalle_desglose import DetalleDesglose
from verifactu.xml.factu.alta.calificacion_operacion import CalificacionOperacion
from verifactu.xml.factu.alta.causa_exencion import CausaExencion
from verifactu.xml.factu.interlocutor import Interlocutor
from verifactu.xml.factu.id_otro import IDOtro
from verifactu.xml.factu.id_type import IDType
from verifactu.xml.factu.codigo_pais import CodigoPais
from verifactu.xml.factu.impuesto import Impuesto
from verifactu.config.settings import Settings
from verifactu.common.utils import Utils
from verifactu.xml.xml_parser import get_xml_date, get_xml_decimal


class Invoice:
    """Invoice business object."""

    def __init__(self, invoice_id: str, invoice_date: datetime, seller_id: str):
        if not invoice_id or not seller_id:
            raise ValueError("invoice_id and seller_id cannot be null or empty.")
        self._data = InvoiceData()
        self._registro_alta_source = None
        self.invoice_id = invoice_id.strip()
        self.invoice_date = invoice_date
        self.seller_id = seller_id.strip().upper()

    @property
    def invoice_id(self) -> str:
        return self._data.invoice_id

    @invoice_id.setter
    def invoice_id(self, value: str):
        self._data.invoice_id = value

    @property
    def invoice_date(self) -> datetime:
        return self._data.invoice_date

    @invoice_date.setter
    def invoice_date(self, value: datetime):
        self._data.invoice_date = value

    @property
    def seller_id(self) -> str:
        return self._data.seller_id

    @seller_id.setter
    def seller_id(self, value: str):
        self._data.seller_id = value

    @property
    def seller_name(self) -> str:
        return self._data.seller_name

    @seller_name.setter
    def seller_name(self, value: str):
        self._data.seller_name = value

    @property
    def buyer_id(self) -> str:
        return self._data.buyer_id

    @buyer_id.setter
    def buyer_id(self, value: str):
        self._data.buyer_id = value

    @property
    def buyer_name(self) -> str:
        return self._data.buyer_name

    @buyer_name.setter
    def buyer_name(self, value: str):
        self._data.buyer_name = value

    @property
    def buyer_country_id(self) -> str:
        return self._data.buyer_country_id

    @buyer_country_id.setter
    def buyer_country_id(self, value: str):
        self._data.buyer_country_id = value

    @property
    def buyer_id_type(self) -> Optional[str]:
        return self._data.buyer_id_type

    @buyer_id_type.setter
    def buyer_id_type(self, value: str):
        self._data.buyer_id_type = value

    @property
    def invoice_type(self) -> Optional[TipoFactura]:
        return self._data.invoice_type

    @invoice_type.setter
    def invoice_type(self, value: TipoFactura):
        self._data.invoice_type = value

    @property
    def rectification_type(self) -> Optional[TipoRectificativa]:
        return self._data.rectification_type

    @rectification_type.setter
    def rectification_type(self, value: TipoRectificativa):
        self._data.rectification_type = value

    @property
    def tax_items(self) -> List[TaxItem]:
        return self._data.tax_items

    @tax_items.setter
    def tax_items(self, value: List[TaxItem]):
        self._data.tax_items = value

    @property
    def total_amount(self) -> float:
        return self._data.total_amount

    @total_amount.setter
    def total_amount(self, value: float):
        self._data.total_amount = value

    @property
    def total_tax_output(self) -> float:
        return self._data.total_tax_output

    @total_tax_output.setter
    def total_tax_output(self, value: float):
        self._data.total_tax_output = value

    @property
    def total_tax_output_surcharge(self) -> float:
        return self._data.total_tax_output_surcharge

    @total_tax_output_surcharge.setter
    def total_tax_output_surcharge(self, value: float):
        self._data.total_tax_output_surcharge = value

    @property
    def total_tax_withheld(self) -> float:
        return self._data.total_tax_withheld

    @total_tax_withheld.setter
    def total_tax_withheld(self, value: float):
        self._data.total_tax_withheld = value

    @property
    def text(self) -> str:
        return self._data.text

    @text.setter
    def text(self, value: str):
        self._data.text = value

    @property
    def rectification_items(self) -> List:
        return self._data.rectification_items

    @rectification_items.setter
    def rectification_items(self, value: List):
        self._data.rectification_items = value

    @property
    def rectification_tax_base(self) -> float:
        return self._data.rectification_tax_base

    @rectification_tax_base.setter
    def rectification_tax_base(self, value: float):
        self._data.rectification_tax_base = value

    @property
    def rectification_tax_amount(self) -> float:
        return self._data.rectification_tax_amount

    @rectification_tax_amount.setter
    def rectification_tax_amount(self, value: float):
        self._data.rectification_tax_amount = value

    @property
    def rectification_tax_amount_surcharge(self) -> float:
        return self._data.rectification_tax_amount_surcharge

    @rectification_tax_amount_surcharge.setter
    def rectification_tax_amount_surcharge(self, value: float):
        self._data.rectification_tax_amount_surcharge = value

    @property
    def operation_date(self):
        return self._data.operation_date

    @operation_date.setter
    def operation_date(self, value):
        self._data.operation_date = value

    def calculate_totals(self):
        """Calcula los totales de la factura."""
        from decimal import Decimal
        self._data.total_amount = Decimal("0")
        self._data.total_tax_output = Decimal("0")
        self._data.total_tax_output_surcharge = Decimal("0")
        self._data.total_tax_withheld = Decimal("0")
        self._data.net_amount = Decimal("0")

        if not self._data.tax_items:
            return

        for tax_item in self._data.tax_items:
            if tax_item.tax_class == TaxClass.TaxOutput:
                self._data.net_amount += tax_item.tax_base
                self._data.total_tax_output += tax_item.tax_amount
                self._data.total_tax_output_surcharge += tax_item.tax_amount_surcharge
            else:
                self._data.total_tax_withheld += tax_item.tax_amount

        self._data.total_amount = (self._data.net_amount
                                   + self._data.total_tax_output
                                   + self._data.total_tax_output_surcharge
                                   - self._data.total_tax_withheld)

    def get_registro_alta(self) -> RegistroAlta:
        """Obtiene el registro de alta para verifactu."""
        if self._registro_alta_source is not None:
            return self._registro_alta_source

        self.calculate_totals()

        total_tax_amount = self._round_away(
            self._data.total_tax_output + self._data.total_tax_output_surcharge, 2)
        total_amount = self._round_away(self._data.total_amount, 2)

        registro_alta = RegistroAlta()
        registro_alta.id_version = Settings.current.id_version
        registro_alta.id_factura_alta = IDFactura()
        registro_alta.id_factura_alta.id_emisor_factura = self.seller_id.strip()
        registro_alta.id_factura_alta.num_serie_factura = self.invoice_id.strip()
        registro_alta.id_factura_alta.fecha_expedicion_factura = get_xml_date(self.invoice_date)
        registro_alta.nombre_razon_emisor = self.seller_name
        registro_alta.tipo_factura = self.invoice_type
        registro_alta.descripcion_operacion = self.text
        registro_alta.destinatarios = self._get_destinatarios()
        registro_alta.desglose = self._get_desglose()
        registro_alta.cuota_total = get_xml_decimal(total_tax_amount)
        registro_alta.importe_total = get_xml_decimal(total_amount)
        registro_alta.sistema_informatico = Settings.current.sistema_informatico
        registro_alta.tipo_huella = TipoHuella.Sha256
        registro_alta.tipo_huella_specified = True

        if self.operation_date:
            registro_alta.fecha_operacion = get_xml_date(self.operation_date)

        is_rectification = self.invoice_type in (
            TipoFactura.R1, TipoFactura.R2, TipoFactura.R3, TipoFactura.R4, TipoFactura.R5)

        if is_rectification:
            if self.rectification_type == TipoRectificativa.S and self.rectification_tax_base != 0:
                registro_alta.importe_rectificacion = ImporteRectificacion()
                registro_alta.importe_rectificacion.base_rectificada = get_xml_decimal(self.rectification_tax_base)
                registro_alta.importe_rectificacion.cuota_rectificada = get_xml_decimal(self.rectification_tax_amount)
                registro_alta.importe_rectificacion.cuota_recargo_rectificado = get_xml_decimal(self.rectification_tax_amount_surcharge)

            if self.rectification_type == TipoRectificativa.NA:
                registro_alta.tipo_rectificativa = TipoRectificativa.I
            registro_alta.tipo_rectificativa_specified = True

        if self.rectification_items:
            ids_factura = []
            for item in self.rectification_items:
                idf = IDFactura()
                idf.id_emisor_factura = self.seller_id
                idf.num_serie_factura = item.invoice_id
                idf.fecha_expedicion_factura = get_xml_date(item.invoice_date)
                ids_factura.append(idf)

            if self.invoice_type == TipoFactura.F3:
                registro_alta.facturas_sustituidas = ids_factura
            else:
                if not is_rectification:
                    raise ValueError(
                        "No se pueden incluir elementos en la lista 'RectificationItems'"
                        " si InvoiceType no es rectificativa (R1, R2, R3, R4, R5).")
                registro_alta.facturas_rectificadas = ids_factura

        if self.rectification_type != TipoRectificativa.NA:
            if not is_rectification:
                raise ValueError(
                    "RectificationType no puede estar asignado (tiene que ser TipoRectificativa.NA)"
                    " si InvoiceType no es rectificativa (R1, R2, R3, R4, R5).")
            registro_alta.tipo_rectificativa = self.rectification_type
            registro_alta.tipo_rectificativa_specified = True

        return registro_alta

    @staticmethod
    def _round_away(value: Decimal, digits: int = 2) -> Decimal:
        """Redondeo AwayFromZero (equivalente a MidpointRounding.AwayFromZero de C#).

        Como Math.Round de C# con decimal, el resultado conserva la
        representación mínima (sin ceros finales).
        """
        from decimal import ROUND_HALF_UP
        quantum = Decimal(1).scaleb(-digits)
        rounded = value.quantize(quantum, rounding=ROUND_HALF_UP)
        if rounded == rounded.to_integral_value():
            return rounded.to_integral_value()
        return rounded.normalize()

    def _get_desglose(self) -> list:
        """Obtiene el desglose de la factura."""
        if not self.tax_items:
            raise ValueError(
                "No se puede obtener el bloque obligatorio 'DetalleDesglose'"
                " ya que la lista de TaxItems no contiene elementos.")

        desglose = []
        for tax_item in self.tax_items:
            detalle = DetalleDesglose()
            detalle.impuesto = tax_item.tax
            detalle.clave_regimen = tax_item.tax_scheme
            detalle.calificacion_operacion = tax_item.tax_type
            detalle.calificacion_operacion_specified = tax_item.tax_exception == CausaExencion.NA
            detalle.tipo_impositivo = get_xml_decimal(
                self._round_away(tax_item.tax_rate, 2))
            detalle.base_imponible_o_importe_no_sujeto = get_xml_decimal(
                self._round_away(tax_item.tax_base, 2))
            detalle.cuota_repercutida = get_xml_decimal(
                self._round_away(tax_item.tax_amount, 2))

            is_n = tax_item.tax_type in (CalificacionOperacion.N1, CalificacionOperacion.N2)
            if is_n and detalle.impuesto == Impuesto.IVA:
                if tax_item.tax_rate + tax_item.tax_amount == 0:
                    detalle.tipo_impositivo = None
                    detalle.cuota_repercutida = None

            if tax_item.tax_exception != CausaExencion.NA:
                detalle.operacion_exenta_specified = True
                detalle.operacion_exenta = tax_item.tax_exception
                detalle.cuota_repercutida = None
                detalle.tipo_impositivo = None

            if tax_item.tax_amount_surcharge != 0:
                detalle.tipo_recargo_equivalencia = get_xml_decimal(
                    self._round_away(tax_item.tax_rate_surcharge, 2))
                detalle.cuota_recargo_equivalencia = get_xml_decimal(
                    self._round_away(tax_item.tax_amount_surcharge, 2))

            detalle.clave_regimen_specified = detalle.impuesto in (
                Impuesto.IVA, Impuesto.IPSI, Impuesto.IGIC)

            desglose.append(detalle)

        return desglose

    def _get_destinatarios(self) -> Optional[list]:
        """Obtiene la lista de destinatarios."""
        # Factura simplificada sin contraparte
        if not self.buyer_id and self.invoice_type in (TipoFactura.F2, TipoFactura.R5):
            return None

        from verifactu.business.validation.nif.tax_id.tax_id_es import TaxIdEs, TaxIdEsException

        is_tax_id_es = False
        try:
            tax_id = TaxIdEs(self.buyer_id)
            is_tax_id_es = tax_id.is_dc_ok
        except TaxIdEsException:
            is_tax_id_es = False
        except Exception as ex:
            Utils.log(f"{ex}")
            if isinstance(ex.__cause__, TaxIdEsException) or isinstance(ex, TaxIdEsException):
                is_tax_id_es = False
            else:
                raise

        if (is_tax_id_es and self.buyer_id_type != IDType.NO_CENSADO
                and (self.buyer_country_id == "ES" or not self.buyer_country_id)):
            interlocutor = Interlocutor()
            interlocutor.nombre_razon = self.buyer_name
            interlocutor.nif = self.buyer_id
            return [interlocutor]

        # Si el campo IDType = "02" (NIF-IVA), no será exigible el campo CodigoPais.
        if self.buyer_id_type == IDType.NIF_IVA and not self.buyer_country_id:
            interlocutor = Interlocutor()
            interlocutor.nombre_razon = self.buyer_name
            interlocutor.id_otro = IDOtro()
            interlocutor.id_otro.id = self.buyer_id
            interlocutor.id_otro.id_type = self.buyer_id_type
            return [interlocutor]

        if not self.buyer_country_id:
            raise ValueError(
                f"Error en factura ({self}): Si BuyerID no es un identificador español válido"
                " (NIF, DNI, NIE...) o IDType = '02' (NIF-IVA) es obligatorio que"
                " BuyerCountryID tenga un valor.")

        try:
            buyer_country_id = CodigoPais(self.buyer_country_id)
        except ValueError:
            raise ValueError(
                f"Error en factura ({self}): El código de pais consignado en"
                f" BuyerCountryID='{self.buyer_country_id}' no es válido.")

        if self.buyer_id_type is None:
            raise ValueError(
                f"Error en factura ({self}): BuyerIDType debe tener un valor válido.")

        interlocutor = Interlocutor()
        interlocutor.nombre_razon = self.buyer_name
        interlocutor.id_otro = IDOtro()
        interlocutor.id_otro.codigo_pais = buyer_country_id
        interlocutor.id_otro.codigo_pais_specified = True
        interlocutor.id_otro.id = self.buyer_id
        interlocutor.id_otro.id_type = self.buyer_id_type
        return [interlocutor]

    def get_registro_anulacion(self) -> RegistroAnulacion:
        """Get RegistroAnulacion from this invoice."""
        registro_anulacion = RegistroAnulacion()
        registro_anulacion.id_version = Settings.current.id_version
        registro_anulacion.id_factura_anulada = IDFactura()
        registro_anulacion.id_factura_anulada.id_emisor_factura_anulada = self.seller_id
        registro_anulacion.id_factura_anulada.num_serie_factura_anulada = self.invoice_id.strip()
        registro_anulacion.id_factura_anulada.fecha_expedicion_factura_anulada = get_xml_date(self.invoice_date)
        registro_anulacion.sistema_informatico = Settings.current.sistema_informatico
        registro_anulacion.tipo_huella = TipoHuella.Sha256
        registro_anulacion.tipo_huella_specified = True
        return registro_anulacion

    def __str__(self) -> str:
        return f"{self.seller_id}-{self.invoice_id}-{get_xml_date(self.invoice_date)}"