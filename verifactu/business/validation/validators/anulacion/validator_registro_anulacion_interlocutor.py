"""Validator - Cancellation interlocutor validator."""

from typing import Optional


class ValidatorRegistroAnulacionInterlocutor:
    """Validator for cancellation interlocutor."""

    @staticmethod
    def validate(registro) -> bool:
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""