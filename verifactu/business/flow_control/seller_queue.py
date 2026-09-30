"""SellerQueue - Queue for sellers."""

from typing import List, Optional


class SellerQueue:
    """Queue for seller data."""
    
    def __init__(self):
        self.sellers: List = []
        self.active: bool = True