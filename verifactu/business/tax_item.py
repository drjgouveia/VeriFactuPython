"""TaxItem - Línea de impuesto."""

from decimal import Decimal
from typing import Optional

from verifactu.business.tax_class import TaxClass
from verifactu.xml.factu.impuesto import Impuesto
from verifactu.xml.factu.alta.clave_regimen import ClaveRegimen
from verifactu.xml.factu.alta.calificacion_operacion import CalificacionOperacion
from verifactu.xml.factu.alta.causa_exencion import CausaExencion


class TaxItem:
    """Representa una línea de impuesto."""

    def __init__(self, tax_class=None, tax=Impuesto.IVA, tax_scheme=ClaveRegimen.RegimenGeneral,
                 tax_type=None, tax_exception=CausaExencion.NA,
                 tax_base=Decimal("0"), tax_rate=Decimal("0"),
                 tax_amount=Decimal("0"), tax_rate_surcharge=Decimal("0"),
                 tax_amount_surcharge=Decimal("0")):
        self.tax_class: Optional[TaxClass] = tax_class or TaxClass.TaxOutput
        self.tax: Impuesto = tax
        self.tax_scheme: Optional[ClaveRegimen] = tax_scheme
        self.tax_type: Optional[CalificacionOperacion] = tax_type
        self.tax_exception: CausaExencion = tax_exception
        self.tax_base: Decimal = Decimal(tax_base)
        self.tax_rate: Decimal = Decimal(tax_rate)
        self.tax_amount: Decimal = Decimal(tax_amount)
        self.tax_rate_surcharge: Decimal = Decimal(tax_rate_surcharge)
        self.tax_amount_surcharge: Decimal = Decimal(tax_amount_surcharge)

    def __str__(self) -> str:
        return f"{self.tax_base}, {self.tax_rate}, {self.tax_amount}"
