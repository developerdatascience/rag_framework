from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter

from src.chunking.base_chunker import BaseChunker

class FixedSizeChunker(BaseChunker):
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 1200, **kwargs):
        super().__init__(chunk_size=chunk_size, chunk_overlap=chunk_overlap, **kwargs)


    def split(self, documents: List[Document]) -> List[Document]:
        splitter = CharacterTextSplitter(
            separator="\n\n",
            chunk_size = self.chunk_size,
            chunk_overlap = self.chunk_overlap,
            length_function=len,
            is_separator_regex=False
        )

        chunks = []
        for doc_index, doc in enumerate(documents):
            split_docs = splitter.split_documents([doc])
            for chunk_index, chunk in enumerate(split_docs):
                meta = dict(chunk.metadata or {})
                meta.update({
                    "doc_index": doc_index,
                    "chunk_index": chunk_index,
                    "chunk_size": self.chunk_size,
                    "chunk_overlap": self.chunk_overlap,
                    "strategy": "fixed"
                })
                chunks.append(Document(page_content=chunk.page_content.strip(), metadata=meta))

        return chunks
