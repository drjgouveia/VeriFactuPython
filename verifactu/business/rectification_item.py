"""RectificationItem - Rectification invoice reference."""

from typing import Optional


class RectificationItem:
    """Reference to a rectified invoice."""

    def __init__(self):
        self.invoice_id: str = ""
        self.invoice_date = None