"""EventChain - Chain of events."""

import os
from threading import Lock
from typing import Optional, Dict, Type

from verifactu.config.settings import Settings
from verifactu.blockchain.chain import Chain


class EventChain(Chain):
    """Event chain for non-Verifactu mode."""
    
    _initialized = False
    
    def __init__(self, seller_id: str):
        super().__init__(seller_id)
    
    def get_chain_dir(self, seller_id: str) -> str:
        return os.path.join(Settings.current.event_chain_path, seller_id)
    
    @classmethod
    def get(cls, seller_id: str) -> 'EventChain':
        return Chain.get_instance(seller_id, EventChain)
    
    @classmethod
    def load_event_chains_from_disk(cls):
        event_chain_path = Settings.current.event_chain_path
        if not event_chain_path or not os.path.exists(event_chain_path):
            raise ValueError(f"EventChainPath is not a valid directory: {event_chain_path}")
        
        for dir_name in os.listdir(event_chain_path):
            dir_path = os.path.join(event_chain_path, dir_name)
            if os.path.isdir(dir_path):
                event_chain = EventChain(dir_name)
                event_chain.read_var()
    
    @classmethod
    def exit(cls):
        Chain.exit_all()