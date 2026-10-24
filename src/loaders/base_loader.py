from abc import ABC, abstractmethod
from typing import List, Dict, Any
from langchain_core.documents import Document

class BaseLoader(ABC):
    def __init__(self, config: Dict[str, Any] | None = None):
        self.config = config or {}

    @abstractmethod
    def load(self, source: str) -> List[Document]:
        """
        Return a list of normalized langchain Document objects.
        """
        raise NotImplementedError

    def normalize_metadata(self, source: str, extra: Dict[str, Any] | None = None) -> Dict[str, Any]:
        meta = {
            "source": source,
            "ingested_at": None
        }
        if extra:
            meta.update(extra)
        return meta

    

