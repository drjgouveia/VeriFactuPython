"""Validator - Tax rate validator."""

from typing import Optional


class ValidatorRegistroAltaDetalleDesgloseTipoImpositivo:
    """Validator for tax rate."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""