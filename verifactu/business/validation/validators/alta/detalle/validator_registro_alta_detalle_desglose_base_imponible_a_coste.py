"""Validator - Base impositive amount at cost validator."""

from typing import Optional


class ValidatorRegistroAltaDetalleDesgloseBaseImponibleACoste:
    """Validator for base imponible at cost."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""