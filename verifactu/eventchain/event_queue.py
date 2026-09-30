"""EventQueue - Queue for events."""

from typing import Dict, List


class EventQueue:
    """Event queue for processing events (modo NO VERI*FACTU)."""

    _initialized = False
    _queues: Dict[str, List] = {}
    
    @classmethod
    def get_queue(cls, seller_id: str) -> List:
        if seller_id not in cls._queues:
            cls._queues[seller_id] = []
        return cls._queues[seller_id]
    
    @classmethod
    def add(cls, seller_id: str, event: dict):
        queue = cls.get_queue(seller_id)
        queue.append(event)
    
    @classmethod
    def process(cls, seller_id: str):
        queue = cls.get_queue(seller_id)
        # Process events here
        pass
    
    @classmethod
    def exit(cls):
        cls._queues.clear()
    
    @classmethod
    def load_event_queue_from_disk(cls):
        # Load events from disk
        pass