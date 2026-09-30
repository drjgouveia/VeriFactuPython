"""DocumentSet - Set of documents."""

from typing import List, Optional
from verifactu.datastore.document import Document


class DocumentSet:
    """Set of documents."""
    
    def __init__(self):
        self.documents: List[Document] = []