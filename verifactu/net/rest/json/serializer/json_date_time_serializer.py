"""JSON DateTime serializer."""

from datetime import datetime


class JsonDateTimeSerializer:
    """Serialize datetime to JSON."""
    
    @staticmethod
    def serialize(value: datetime) -> str:
        return value.isoformat()
    
    @staticmethod
    def deserialize(value: str) -> datetime:
        return datetime.fromisoformat(value)