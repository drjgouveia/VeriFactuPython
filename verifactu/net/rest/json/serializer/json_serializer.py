"""JSON Serializer factory."""

from typing import Any, Optional


class JsonSerializer:
    """JSON serializer factory."""
    
    @staticmethod
    def serialize(obj: Any) -> str:
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        return str(obj)
    
    @staticmethod
    def deserialize(json_str: str, cls=None) -> Any:
        return json_str