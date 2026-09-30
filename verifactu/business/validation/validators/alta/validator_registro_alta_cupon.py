"""Validator - Receipt validator."""

from typing import Optional


class ValidatorRegistroAltaCupon:
    """Validator for coupon field."""

    @staticmethod
    def validate(registro) -> bool:
        """Validate the coupon."""
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""