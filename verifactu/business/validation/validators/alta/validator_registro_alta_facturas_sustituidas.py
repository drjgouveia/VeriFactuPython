"""Validator - Substituted invoices validator."""

from typing import Optional


class ValidatorRegistroAltaFacturasSustituidas:
    """Validator for substituted invoices."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""