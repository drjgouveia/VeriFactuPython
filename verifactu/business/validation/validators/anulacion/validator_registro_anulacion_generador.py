"""Validator - Cancellation issuer validator."""

from typing import Optional


class ValidatorRegistroAnulacionGenerador:
    """Validator for cancellation issuer."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""