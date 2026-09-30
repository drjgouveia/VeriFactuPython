"""Validator - Invoice record validator."""

from typing import Optional


class ValidatorRegistroFactura:
    """Validator for invoice records."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""