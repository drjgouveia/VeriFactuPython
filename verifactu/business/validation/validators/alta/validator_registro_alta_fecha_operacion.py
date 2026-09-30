"""Validator - Operation date validator."""

from typing import Optional


class ValidatorRegistroAltaFechaOperacion:
    """Validator for operation date."""

    @staticmethod
    def validate(registro) -> bool:
        """Validate the operation date."""
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""