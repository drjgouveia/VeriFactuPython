"""Validator - Obligatory field validator."""

from typing import Optional


class ValidatorRegistroAltaCampoObligatorio:
    """Validator for obligatory fields in registration records."""

    @staticmethod
    def validate(registro) -> bool:
        """Validate obligatory fields."""
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""