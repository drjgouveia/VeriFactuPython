"""Common utilities for VeriFactu."""

import hashlib
import logging
from typing import Optional, Type, TypeVar

from verifactu.config.settings import Settings
from verifactu.xml.factu.tipo_huella import TipoHuella

T = TypeVar('T')


class Utils:
    """General utility functions for VeriFactu."""

    _hash_algorithms = {
        TipoHuella.Sha256: hashlib.sha256,
    }

    _encodings = {
        "UTF-8": "utf-8",
    }

    _encoding = None
    _logger = None

    @classmethod
    def get_encoding(cls):
        if cls._encoding is None:
            cls._encoding = cls._encodings.get(
                Settings.current.veri_factu_hash_input_encoding, "utf-8")
        return cls._encoding

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            cls._logger = logging.getLogger("verifactu")
        return cls._logger

    @classmethod
    def encoding_encode(cls, text: str) -> bytes:
        """Encode text using the configured encoding."""
        return text.encode(cls.get_encoding())

    @classmethod
    def compute_hash(cls, input_bytes: bytes) -> bytes:
        """Compute hash using the configured algorithm."""
        algorithm = cls._hash_algorithms.get(
            Settings.current.veri_factu_hash_algorithm)
        if algorithm is None:
            raise ValueError(f"Unknown hash algorithm: {Settings.current.veri_factu_hash_algorithm}")
        return algorithm(input_bytes).digest()

    @classmethod
    def log(cls, msg: str):
        """Log a message if logging is enabled."""
        if Settings.current.logging_enabled:
            cls.get_logger().info(msg)

    @classmethod
    def get_encoded_to_hex(cls, text: str) -> str:
        """Codifica un texto a bytes con la codificación configurada y
        devuelve la cadena hexadecimal."""
        return cls.encoding_encode(text).hex().upper()

    @classmethod
    def get_from_encoded_to_hex(cls, text: str) -> str:
        """Decodifica una cadena hexadecimal a texto con la codificación
        configurada."""
        if not text or len(text) % 2 != 0:
            raise ValueError("La cadena de entrada no es válida.")
        return bytes.fromhex(text).decode(cls.get_encoding())

    @classmethod
    def get_xml_enum_value(cls, value) -> Optional[str]:
        """Get the XML enum value from an enum member."""
        if value is None:
            return None
        xml_value = getattr(value, '_xml_value', None)
        if xml_value is not None:
            return xml_value
        return value.value if hasattr(value, 'value') else str(value)

    @classmethod
    def get_enum_from_xml_value(cls, enum_type: Type[T], value: str) -> T:
        """Get an enum member from its XML value."""
        for member in enum_type:
            if getattr(member, '_xml_value', None) == value or member.value == value:
                return member
        raise ValueError(f"No XML value '{value}' for enum {enum_type.__name__}")