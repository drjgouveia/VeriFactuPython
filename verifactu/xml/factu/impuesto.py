"""Enum: Impuesto - Clave que identifica un impuesto."""

from enum import Enum


class Impuesto(Enum):
    """Clave que identifica un impuesto. Alfanumérico(2) L1."""
    IVA = "01"
    IPSI = "02"
    IGIC = "03"
    OTROS = "05"