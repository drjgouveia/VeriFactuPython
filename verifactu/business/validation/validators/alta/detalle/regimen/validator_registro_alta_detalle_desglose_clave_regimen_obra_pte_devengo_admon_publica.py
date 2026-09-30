"""Validator - Public administration work regime key validator."""

from typing import Optional


class ValidatorRegistroAltaDetalleDesgloseClaveRegimenObraPteDevengoAdmonPublica:
    """Validator for public administration work regime key."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""