"""JSON Int serializer."""


class JsonIntSerializer:
    """Serialize integer to JSON."""
    
    @staticmethod
    def serialize(value: int) -> str:
        return str(value)
    
    @staticmethod
    def deserialize(value: str) -> int:
        return int(value)