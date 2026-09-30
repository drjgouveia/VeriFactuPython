"""Tests de hash de RegistroAlta.

Verifica la compatibilidad con la librería .NET original:
el ejemplo 1 del README de https://github.com/mdiago/VeriFactu.
"""

import unittest
from datetime import datetime
from decimal import Decimal

from verifactu import Invoice, TaxItem, RegistroAlta
from verifactu.xml.factu.encadenamiento import Encadenamiento
from verifactu.xml.factu.registro_anterior import RegistroAnterior


class HashTests(unittest.TestCase):

    def _make_invoice(self):
        invoice = Invoice("GITHUB-EJ-003", datetime(2024, 11, 4), "B72877814")
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
        return invoice

    def test_hash_output_matches_dotnet_library(self):
        """Ejemplo 1 del README de la librería .NET."""
        registro = self._make_invoice().get_registro_alta()

        # Forzamos el valor de FechaHoraHusoGenRegistro para que coincida
        registro.fecha_hora_huso_gen_registro = "2024-11-04T12:36:39+01:00"

        # Establecemos el valor del encadenamiento anterior
        registro.encadenamiento = Encadenamiento()
        registro.encadenamiento.registro_anterior = RegistroAnterior()
        registro.encadenamiento.registro_anterior.huella = (
            "8C8DCEFB120522E0C71BC19902F44D5334FF6C98E74F0E3AC1D1E5A30C2EA836")

        self.assertEqual(
            registro.get_hash_output(),
            "4EECCE4DD48C0539665385D61D451BA921B7160CA6FEF46CD3C2E2BC5C778E14")

    def test_hash_input_text(self):
        registro = self._make_invoice().get_registro_alta()
        registro.fecha_hora_huso_gen_registro = "2024-11-04T12:36:39+01:00"
        registro.encadenamiento = Encadenamiento()
        registro.encadenamiento.registro_anterior = RegistroAnterior()
        registro.encadenamiento.registro_anterior.huella = (
            "8C8DCEFB120522E0C71BC19902F44D5334FF6C98E74F0E3AC1D1E5A30C2EA836")

        self.assertEqual(
            registro.get_hash_text_input(),
            "IDEmisorFactura=B72877814"
            "&NumSerieFactura=GITHUB-EJ-003"
            "&FechaExpedicionFactura=04-11-2024"
            "&TipoFactura=F1"
            "&CuotaTotal=21.4"
            "&ImporteTotal=131.4"
            "&Huella=8C8DCEFB120522E0C71BC19902F44D5334FF6C98E74F0E3AC1D1E5A30C2EA836"
            "&FechaHoraHusoGenRegistro=2024-11-04T12:36:39+01:00")

    def test_url_validate(self):
        """Ejemplo 2 del README de la librería .NET."""
        invoice = self._make_invoice()
        invoice.invoice_id = "GITHUB-EJ-004"
        registro = invoice.get_registro_alta()
        url = registro.get_url_validate()
        self.assertEqual(
            url,
            "https://prewww2.aeat.es/wlpl/TIKE-CONT/ValidarQR"
            "?nif=B72877814&numserie=GITHUB-EJ-004&fecha=04-11-2024&importe=131.4")


if __name__ == "__main__":
    unittest.main()
