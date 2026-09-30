"""Enum: IDType - Clave para establecer el tipo de identificación."""

from enum import Enum


class IDType(Enum):
    """Clave para establecer el tipo de identificación en el país de residencia. L7."""
    NIF_IVA = "02"
    PASAPORTE = "03"
    DOCUMENTO_OFICIAL = "04"
    CERTIFICADO_RESIDENCIA = "05"
    OTRO_DOC_PROBATORIO = "06"
    NO_CENSADO = "07"