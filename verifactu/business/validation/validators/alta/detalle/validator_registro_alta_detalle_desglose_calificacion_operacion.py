"""Validator - Operation classification validator."""

from typing import Optional


class ValidatorRegistroAltaDetalleDesgloseCalificacionOperacion:
    """Validator for operation classification."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""