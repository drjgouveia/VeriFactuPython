"""JSON Attribute for serializer."""

from dataclasses import dataclass


@dataclass
class JsonAttribute:
    """Attribute for JSON serialization."""
    exclude_on_default: bool = False
    name: Optional[str] = None