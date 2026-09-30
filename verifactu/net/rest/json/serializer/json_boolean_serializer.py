"""JSON Boolean serializer."""

from verifactu.net.rest.json.json_serializable import JsonSerializable


class JsonBooleanSerializer:
    """Serialize boolean values to JSON."""
    
    @staticmethod
    def serialize(value: bool) -> str:
        return str(value).lower()
    
    @staticmethod
    def deserialize(value: str) -> bool:
        return value.lower() == 'true'