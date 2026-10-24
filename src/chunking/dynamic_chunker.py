from typing import List, Dict, Any
from langchain_core.documents import Document

from src.chunking.base_chunker import BaseChunker
from src.chunking.fixed_chunker import FixedSizeChunker
from src.chunking.recursive_chunker import RecursiveChunker
from src.chunking.semantic_chunker import SemanticChunkerWrapper
from src.chunking.strategy_selector import StrategySelector

class DynamicChunker(BaseChunker):
    def __init__(self, **kwargs):
        self.selector = StrategySelector(default_strategy="recursive")
        self.kwargs = kwargs

    def _instantiate_strategy(self, strategy_name: str, chunk_size: int, chunk_overlap: int):
        if strategy_name == "fixed_size":
            return FixedSizeChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        elif strategy_name == "recursive":
            return RecursiveChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        elif strategy_name == "semantic":
            return SemanticChunkerWrapper(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        else:
            return RecursiveChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)


    def split(self, documents: List[Document]) -> List[Document]:
        if not documents:
            return []
        best_candidate = self.selector.select(documents)
        strategy = self._instantiate_strategy(
            best_candidate.name,
            best_candidate.chunk_size,
            best_candidate.chunk_overlap
        )

        chunks = strategy.split(documents)

        for i, chunk in enumerate(chunks):
            meta = dict(chunk.metadata or {})
            meta.update({
                "selected_strategy": best_candidate.name,
                "selected_chunk_size": best_candidate.chunk_size,
                "selected_chunk_overlap": best_candidate.chunk_overlap
            })
            chunks[i] = Document(page_content=chunk.page_content.strip(), metadata=meta)

        return chunks

        

