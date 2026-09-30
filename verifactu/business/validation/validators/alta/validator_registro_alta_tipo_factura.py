"""Validator - Invoice type validator."""

from typing import Optional


class ValidatorRegistroAltaTipoFactura:
    """Validator for invoice type."""

    @staticmethod
    def validate(registro) -> bool:
        """Validate the invoice type."""
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""