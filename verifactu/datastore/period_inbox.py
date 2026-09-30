"""PeriodInbox - Period inbox."""

from typing import Optional
from verifactu.datastore.period_box import PeriodBox


class PeriodInbox(PeriodBox):
    """Period inbox for incoming documents."""
    
    def __init__(self):
        super().__init__()