"""InvoiceAction - Action types for invoice operations."""

from enum import Enum


class InvoiceActionType(Enum):
    """Invoice action types."""
    Create = "Create"
    Cancel = "Cancel"
    Fix = "Fix"