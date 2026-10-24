from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from langchain_core.documents import Document

class BaseRetriever(ABC):
    @abstractmethod
    def retrieve(self, query: str, k: int = 5, filters: Optional[Dict[str, Any]] = None) -> List[Document]:
        pass