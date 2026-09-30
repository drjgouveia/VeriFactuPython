"""Tests de fechas xml (XmlDateTests de .NET)."""

import unittest
from datetime import datetime

from verifactu import get_xml_date, get_xml_date_time_iso8601


class XmlDateTests(unittest.TestCase):

    def test_spanish_culture_keeps_the_expedition_date(self):
        self.assertEqual("15-01-2024", get_xml_date(datetime(2024, 1, 15)))

    def test_date_time_iso8601(self):
        result = get_xml_date_time_iso8601(datetime(2024, 11, 4, 12, 36, 39))
        self.assertEqual(result, "2024-11-04T12:36:39")

    def test_default_date(self):
        self.assertEqual("01-01-0001", get_xml_date(None))


if __name__ == "__main__":
    unittest.main()
