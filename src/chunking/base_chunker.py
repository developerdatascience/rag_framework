from langchain_core.documents import Document
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseChunker(ABC):
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 1200, **kwargs):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.kwargs = kwargs


    @abstractmethod
    def split(self, documents: List[Document]) ->List[Document]:
        """
        Takes a list of LangChain documents and returns chunked documents.
        """
        raise NotImplementedError

    def enrich_metadata(self, doc: Document, chunk_index: int, chunk_size: int, overlap: int, strategy: str):
        meta = dict(doc.metadata or {})
        meta.update({
            "chunk_index": chunk_index,
            "chunk_size": chunk_size,
            "chunk_overlap": overlap,
            "chunk_strategy": strategy
        })
        return Document(page_content=doc.page_content.strip(), metadata=meta)