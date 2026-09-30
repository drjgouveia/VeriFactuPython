"""Eventos de negocio (modo NO VERI*FACTU)."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class EventData:
    """Datos de un evento de negocio."""

    event_type: str = ""
    description: str = ""
    timestamp: Optional[datetime] = None
    data: dict = field(default_factory=dict)


@dataclass
class EventEntry:
    """Entrada de evento en la cola."""

    event: EventData = None
    processed: bool = False
    error: Optional[str] = None


class EventFactory:
    """Fábrica de eventos."""

    @staticmethod
    def create(event_type: str, description: str = "",
               data: dict = None) -> EventData:
        return EventData(
            event_type=event_type,
            description=description,
            timestamp=datetime.now(),
            data=data or {},
        )
