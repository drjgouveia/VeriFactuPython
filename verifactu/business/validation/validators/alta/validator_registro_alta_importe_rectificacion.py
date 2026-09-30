"""Validator - Rectification amount validator."""

from typing import Optional


class ValidatorRegistroAltaImporteRectificacion:
    """Validator for rectification amounts."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""