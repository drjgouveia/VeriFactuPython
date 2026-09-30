"""Validator base class."""

from abc import ABC, abstractmethod
from typing import Optional


class IValidator(ABC):
    """Validator interface."""

    @abstractmethod
    def validate(self, value) -> bool:
        pass

    @abstractmethod
    def get_error_message(self) -> str:
        pass