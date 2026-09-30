"""Validator - Exempt operation validator."""

from typing import Optional


class ValidatorRegistroAltaDetalleDesgloseOperacionExenta:
    """Validator for exempt operations."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""