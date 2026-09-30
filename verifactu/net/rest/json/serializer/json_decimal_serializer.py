"""JSON Decimal serializer."""

from decimal import Decimal


class JsonDecimalSerializer:
    """Serialize Decimal to JSON."""
    
    @staticmethod
    def serialize(value: Decimal) -> str:
        return str(value)
    
    @staticmethod
    def deserialize(value: str) -> Decimal:
        return Decimal(value)