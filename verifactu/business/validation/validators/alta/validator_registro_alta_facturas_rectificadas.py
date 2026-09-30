"""Validator - Rectified invoices validator."""

from typing import Optional


class ValidatorRegistroAltaFacturasRectificadas:
    """Validator for rectified invoices."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""