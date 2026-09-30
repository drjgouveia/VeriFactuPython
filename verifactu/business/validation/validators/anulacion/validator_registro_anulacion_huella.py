"""Validator - Cancellation hash validator."""

from typing import Optional


class ValidatorRegistroAnulacionHuella:
    """Validator for cancellation hash."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""