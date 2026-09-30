"""JSON default serializer."""

from verifactu.net.rest.json.json_serializable import JsonSerializable


class JsonDefaultSerializer:
    """Default JSON serializer."""
    
    @staticmethod
    def serialize(obj) -> str:
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        return str(obj)