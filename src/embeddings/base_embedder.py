from abc import abstractmethod
from typing import List

from langchain_core.embeddings import Embeddings


class BaseEmbedder(Embeddings):
    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        pass

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        pass