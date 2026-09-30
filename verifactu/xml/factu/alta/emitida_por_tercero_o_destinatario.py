"""Enum: EmitidaPorTerceroODestinatario - Emitter type codes."""

from enum import Enum


class EmitidaPorTerceroODestinatario(Enum):
    """Indica si la factura fue emitida por tercero o destinatario."""
    T = "T"
    D = "D"