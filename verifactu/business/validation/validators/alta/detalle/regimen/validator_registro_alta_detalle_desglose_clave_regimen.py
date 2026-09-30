"""Validator - Regime key validator (base)."""

from typing import Optional


class ValidatorRegistroAltaDetalleDesgloseClaveRegimen:
    """Validator for regime key."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""