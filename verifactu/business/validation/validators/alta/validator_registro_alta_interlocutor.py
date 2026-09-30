"""Validator - Interlocutor (counter-party) validator."""

from typing import Optional


class ValidatorRegistroAltaInterlocutor:
    """Validator for interlocutor/counter-party."""

    @staticmethod
    def validate(registro) -> bool:
        """Validate the interlocutor."""
        return True

    @staticmethod
    def get_error_message() -> str:
        return ""