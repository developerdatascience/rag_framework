from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from langchain_core.documents import Document

class BaseVectorStore(ABC):
    @abstractmethod
    def add_documents(self, documents: List[Document]) -> None:
        pass

    @abstractmethod
    def similarity_search(self, query: str, k: int = 5, filter: Optional[Dict[str, Any]] = None) -> List[Document]:
        pass

    @abstractmethod
    def save_local(self, path: str) -> None:
        pass

    @abstractmethod
    def load_local(self, path: str) -> None:
        pass