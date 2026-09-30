"""Validator - Export regime key validator."""

from typing import Optional


class ValidatorRegistroAltaDetalleDesgloseClaveRegimenExportacion:
    """Validator for export regime key."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""