"""Validator - Text validator."""

from typing import Optional


class ValidatorText:
    """Validator for text fields."""

    @staticmethod
    def validate(value) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""