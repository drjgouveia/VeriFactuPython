"""Tests de redondeo de totales de factura (InvoiceTotalRoundTests de .NET)."""

import unittest
from datetime import datetime
from decimal import Decimal

from verifactu import Invoice, TaxItem, TipoFactura


class InvoiceTotalRoundTests(unittest.TestCase):

    def test_totals_round_to_two_decimals(self):
        invoice = Invoice("TEST-ROUND", datetime(2024, 11, 15), "B72877814")
        invoice.invoice_type = TipoFactura.F2
        invoice.seller_name = "WEFINZ GANDIA SL"
        tax_item = TaxItem()
        tax_item.tax_base = Decimal("10.00")
        tax_item.tax_rate = Decimal("21.00")
        tax_item.tax_amount = Decimal("2.10")
        invoice.tax_items = [tax_item]

        alta = invoice.get_registro_alta()

        self.assertEqual(alta.cuota_total, "2.1")
        self.assertEqual(alta.importe_total, "12.1")

    def test_readme_example_totals(self):
        invoice = Invoice("GIT-EJ-0002", datetime(2024, 11, 15), "B72877814")
        invoice.seller_name = "WEFINZ GANDIA SL"
        invoice.buyer_id = "B44531218"
        invoice.buyer_name = "WEFINZ SOLUTIONS SL"
        tax_item_1 = TaxItem()
        tax_item_1.tax_rate = Decimal("4")
        tax_item_1.tax_base = Decimal("10")
        tax_item_1.tax_amount = Decimal("0.4")
        tax_item_2 = TaxItem()
        tax_item_2.tax_rate = Decimal("21")
        tax_item_2.tax_base = Decimal("100")
        tax_item_2.tax_amount = Decimal("21")
        invoice.tax_items = [tax_item_1, tax_item_2]

        alta = invoice.get_registro_alta()

        self.assertEqual(alta.cuota_total, "21.4")
        self.assertEqual(alta.importe_total, "131.4")


if __name__ == "__main__":
    unittest.main()
