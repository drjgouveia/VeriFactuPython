"""Validator - Third party collection regime key validator."""

from typing import Optional


class ValidatorRegistroAltaDetalleDesgloseClaveRegimenCobroTerceros:
    """Validator for third party collection regime key."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""