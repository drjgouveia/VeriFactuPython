"""Tests de validación de NIF español (TaxIdEs)."""

import unittest

from verifactu import TaxIdEs, TaxIdEsException


class TaxIdEsTests(unittest.TestCase):

    def test_valid_company_nif(self):
        tax_id = TaxIdEs("B72877814")
        self.assertTrue(tax_id.is_dc_ok)
        self.assertEqual(tax_id.person_type.value, "LegalEntity")

    def test_valid_dni(self):
        tax_id = TaxIdEs("12345678Z")
        self.assertTrue(tax_id.is_dc_ok)
        self.assertEqual(tax_id.person_type.value, "Individual")

    def test_invalid_dni(self):
        tax_id = TaxIdEs("12345678A")
        self.assertFalse(tax_id.is_dc_ok)

    def test_invalid_format_does_not_raise(self):
        # Al igual que en la librería .NET, un formato no válido no lanza
        # excepción: se registra el error y IsDCOK queda a False.
        tax_id = TaxIdEs("XYZ")
        self.assertFalse(tax_id.is_dc_ok)

    def test_invalid_legal_entity_pattern_raises(self):
        # 9 caracteres con letra final no válida para persona jurídica
        with self.assertRaises(TaxIdEsException):
            TaxIdEs("B7287781X")

    def test_nie_x(self):
        # X0000000T es el NIE de ejemplo más simple válido
        tax_id = TaxIdEs("X0000000T")
        self.assertTrue(tax_id.is_dc_ok)


if __name__ == "__main__":
    unittest.main()
