"""Seller - Seller entity."""

from typing import Optional


class Seller:
    """Seller entity."""
    
    def __init__(self):
        self.seller_id: str = ""
        self.name: str = ""
        self.nif: str = ""
        self.is_active: bool = True
    
    @staticmethod
    def get_sellers() -> list:
        """Get all sellers."""
        return []