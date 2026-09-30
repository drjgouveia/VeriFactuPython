"""Validator - Recipient validator."""

from typing import Optional


class ValidatorRegistroAltaDestinatarios:
    """Validator for recipients."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""