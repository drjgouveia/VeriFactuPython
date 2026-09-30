"""InvoiceData - Plain data object de factura."""

from decimal import Decimal
from typing import List, Optional

from verifactu.xml.factu.alta.tipo_factura import TipoFactura
from verifactu.xml.factu.alta.tipo_rectificativa import TipoRectificativa
from verifactu.business.tax_item import TaxItem
from verifactu.business.rectification_item import RectificationItem


class InvoiceData:
    """Plain data object con los datos de una factura."""

    def __init__(self):
        self.invoice_id: str = ""
        self.invoice_date = None
        self.operation_date = None
        self.seller_id: str = ""
        self.seller_name: str = ""
        self.buyer_id: str = ""
        self.buyer_name: str = ""
        self.buyer_country_id: str = ""
        self.buyer_id_type = None
        self.invoice_type: TipoFactura = TipoFactura.F1
        self.rectification_type: TipoRectificativa = TipoRectificativa.NA
        self.tax_items: List[TaxItem] = []
        self.total_amount: Decimal = Decimal("0")
        self.total_tax_output: Decimal = Decimal("0")
        self.total_tax_output_surcharge: Decimal = Decimal("0")
        self.total_tax_withheld: Decimal = Decimal("0")
        self.net_amount: Decimal = Decimal("0")
        self.text: str = ""
        self.rectification_items: List[RectificationItem] = []
        self.rectification_tax_base: Decimal = Decimal("0")
        self.rectification_tax_amount: Decimal = Decimal("0")
        self.rectification_tax_amount_surcharge: Decimal = Decimal("0")
        self.service_key: str = ""
