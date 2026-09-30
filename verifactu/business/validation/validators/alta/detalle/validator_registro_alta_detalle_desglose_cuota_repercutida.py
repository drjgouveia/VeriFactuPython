"""Validator - Repercuted tax validator."""

from typing import Optional


class ValidatorRegistroAltaDetalleDesgloseCuotaRepercutida:
    """Validator for repercuted tax."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""