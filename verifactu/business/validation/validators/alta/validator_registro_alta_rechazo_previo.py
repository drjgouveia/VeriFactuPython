"""Validator - Rejection previous validator."""

from typing import Optional


class ValidatorRegistroAltaRechazoPrevio:
    """Validator for previous rejection."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""