"""Validator - Third party validator."""

from typing import Optional


class ValidatorRegistroAltaTercero:
    """Validator for third party."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""