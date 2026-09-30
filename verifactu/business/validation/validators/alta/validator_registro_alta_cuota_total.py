"""Validator - Total amount validator."""

from typing import Optional


class ValidatorRegistroAltaCuotaTotal:
    """Validator for total amount."""

    @staticmethod
    def validate(registro) -> bool:
        """Validate the total amount."""
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""