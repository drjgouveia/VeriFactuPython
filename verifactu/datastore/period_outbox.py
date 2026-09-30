"""PeriodOutbox - Period outbox."""

from typing import Optional
from verifactu.datastore.period_box import PeriodBox


class PeriodOutbox(PeriodBox):
    """Period outbox for outgoing documents."""
    
    def __init__(self):
        super().__init__()