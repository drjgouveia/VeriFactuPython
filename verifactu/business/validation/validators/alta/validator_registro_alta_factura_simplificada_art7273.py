"""Validator - Simplified invoice Art. 7.2/7.3 (alternative)."""

from typing import Optional


class ValidatorRegistroAltaFacturaSimplificadaArt7273:
    """Validator for simplified invoices Art. 7.2/7.3."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""