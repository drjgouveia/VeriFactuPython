"""Validator - Invoice without recipient identification (Art. 6.1.d)."""

from typing import Optional


class ValidatorRegistroAltaFacturaSinIdentifDestinatarioArt61d:
    """Validator for invoices without recipient ID."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""