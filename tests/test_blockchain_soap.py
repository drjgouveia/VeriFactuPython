"""Tests de la cadena de bloques y el sobre SOAP."""

import os
import unittest
from datetime import datetime
from decimal import Decimal

from verifactu import Invoice, TaxItem, TipoFactura, Blockchain
from verifactu.xml.xml_parser import XmlParser
from verifactu.xml.namespaces import Items


class BlockchainTests(unittest.TestCase):

    def setUp(self):
        import shutil
        from verifactu.config.settings import Settings
        from verifactu.blockchain.blockchain import Blockchain
        # Estado limpio por prueba: eliminamos la cadena del emisor
        chain_dir = os.path.join(Settings.current.blockchain_path, "B72877814")
        if os.path.exists(chain_dir):
            shutil.rmtree(chain_dir)
        Blockchain._instances.clear()
        Blockchain._initialized = False

    def _make_invoice(self, num):
        invoice = Invoice(num, datetime(2024, 10, 14), "B72877814")
        invoice.invoice_type = TipoFactura.F1
        invoice.seller_name = "WEFINZ GANDIA SL"
        invoice.buyer_id = "B44531218"
        invoice.buyer_name = "WEFINZ SOLUTIONS SL"
        invoice.text = "PRESTACION SERVICIOS DESARROLLO SOFTWARE"
        t1 = TaxItem()
        t1.tax_rate = Decimal("4")
        t1.tax_base = Decimal("10")
        t1.tax_amount = Decimal("0.4")
        t2 = TaxItem()
        t2.tax_rate = Decimal("21")
        t2.tax_base = Decimal("100")
        t2.tax_amount = Decimal("21")
        invoice.tax_items = [t1, t2]
        return invoice

    def test_blockchain_chain(self):
        """Ejemplo 4 del README de la librería .NET."""
        registro_first = self._make_invoice("TEST001").get_registro_alta()
        blockchain = Blockchain.get("B72877814")
        blockchain.add(registro_first)

        registro_second = self._make_invoice("TEST002").get_registro_alta()
        blockchain.add(registro_second)

        # El encadenamiento del segundo apunta a la huella del primero
        self.assertEqual(
            registro_second.encadenamiento.registro_anterior.huella,
            registro_first.get_hash_output())

        self.assertEqual(registro_first.blockchain_link_id, 1)
        self.assertEqual(registro_second.blockchain_link_id, 2)
        self.assertEqual(registro_first.ref_externa, "00000000000000000001")


class SoapEnvelopeTests(unittest.TestCase):

    def _make_invoice(self):
        invoice = Invoice("GIT-EJ-0002", datetime(2024, 11, 15), "B72877814")
        invoice.invoice_type = TipoFactura.F1
        invoice.seller_name = "WEFINZ GANDIA SL"
        invoice.buyer_id = "B44531218"
        invoice.buyer_name = "WEFINZ SOLUTIONS SL"
        invoice.text = "PRESTACION SERVICIOS DESARROLLO SOFTWARE"
        t1 = TaxItem()
        t1.tax_rate = Decimal("4")
        t1.tax_base = Decimal("10")
        t1.tax_amount = Decimal("0.4")
        t2 = TaxItem()
        t2.tax_rate = Decimal("21")
        t2.tax_base = Decimal("100")
        t2.tax_amount = Decimal("21")
        invoice.tax_items = [t1, t2]
        return invoice

    def test_soap_envelope_structure(self):
        from verifactu.business.invoice_entry import InvoiceEntry
        entry = InvoiceEntry(self._make_invoice())
        xml = entry.get_xml().decode()

        self.assertTrue(xml.startswith("<soapenv:Envelope"))
        self.assertIn("<soapenv:Body>", xml)
        self.assertIn("<sum:RegFactuSistemaFacturacion>", xml)
        self.assertIn("<sum:Cabecera>", xml)
        self.assertIn("<sum1:ObligadoEmision>", xml)
        self.assertIn("<sum1:RegistroAlta>", xml)
        self.assertIn("<sum1:IDFactura>", xml)
        self.assertIn("<sum1:NumSerieFactura>GIT-EJ-0002</sum1:NumSerieFactura>", xml)
        self.assertIn("<sum1:CuotaTotal>21.4</sum1:CuotaTotal>", xml)
        self.assertIn("<sum1:ImporteTotal>131.4</sum1:ImporteTotal>", xml)

    def test_validation_rejects_missing_seller_name(self):
        from verifactu.business.invoice_entry import InvoiceEntry
        invoice = self._make_invoice()
        invoice.seller_name = None
        with self.assertRaises(ValueError):
            InvoiceEntry(invoice)


if __name__ == "__main__":
    unittest.main()
