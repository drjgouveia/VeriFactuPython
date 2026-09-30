"""Validator - Local business lease regime key validator."""

from typing import Optional


class ValidatorRegistroAltaDetalleDesgloseClaveRegimenArrendamientoLocalNecocio:
    """Validator for local business lease regime key."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""