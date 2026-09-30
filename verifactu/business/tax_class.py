"""TaxClass - Tax classification."""

from enum import Enum


class TaxClass(Enum):
    """Tax class: output or withheld."""
    TaxOutput = "TaxOutput"
    TaxWithheld = "TaxWithheld"