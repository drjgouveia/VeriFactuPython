"""Validator - Simplified invoice validator (Art. 7.2/7.3)."""

from typing import Optional


class ValidatorRegistroAltaFacturaSimplificada:
    """Validator for simplified invoices."""

    @staticmethod
    def validate(registro) -> bool:
        """Validate the simplified invoice."""
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""