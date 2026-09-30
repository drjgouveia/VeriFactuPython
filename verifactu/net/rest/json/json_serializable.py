"""JSON serializer base class for VeriFactu."""

import json
from typing import Optional, Dict, Any


class JsonSerializable:
    """Base class for JSON serializable objects."""
    
    def __init__(self):
        self._service_key: str = ""
    
    @property
    def service_key(self) -> str:
        return self._service_key
    
    @service_key.setter
    def service_key(self, value: str):
        self._service_key = value
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.__dict__, default=str, ensure_ascii=False)
    
    def from_json(self, json_str: str) -> 'JsonSerializable':
        """Load from JSON string."""
        data = json.loads(json_str)
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
    
    def __str__(self) -> str:
        return self.to_json()