"""DocumentBox - Document container."""

from typing import List, Optional
from verifactu.datastore.document import Document


class DocumentBox:
    """Container for documents."""
    
    def __init__(self):
        self.documents: List[Document] = []