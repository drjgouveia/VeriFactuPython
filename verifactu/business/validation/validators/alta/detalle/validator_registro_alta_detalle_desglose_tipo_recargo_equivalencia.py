"""Validator - Surcharge rate validator."""

from typing import Optional


class ValidatorRegistroAltaDetalleDesgloseTipoRecargoEquivalencia:
    """Validator for surcharge rate."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""