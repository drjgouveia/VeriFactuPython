"""Validator - Third party emission validator."""

from typing import Optional


class ValidatorRegistroAltaEmitidaPorTerceroODestinatario:
    """Validator for third-party emission."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""