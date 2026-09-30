"""Validator - Simplified regime key validator."""

from typing import Optional


class ValidatorRegistroAltaDetalleDesgloseClaveRegimenRegimenSimplificado:
    """Validator for simplified regime key."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""