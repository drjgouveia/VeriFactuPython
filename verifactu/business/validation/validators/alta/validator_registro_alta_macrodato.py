"""Validator - Macro data validator."""

from typing import Optional


class ValidatorRegistroAltaMacrodato:
    """Validator for macro data."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""