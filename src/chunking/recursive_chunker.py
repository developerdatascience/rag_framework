from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.chunking.base_chunker import BaseChunker


class RecursiveChunker(BaseChunker):
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 120, seperators: List[str] | None = None, **kwargs) -> None:
        super().__init__(chunk_size=chunk_size, chunk_overlap=chunk_overlap, **kwargs)
        self.seperators = seperators or ["\n\n", "\n", " ", ""]


    def split(self, documents: List[Document]) -> List[Document]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.chunk_size,
            chunk_overlap = self.chunk_overlap,
            length_function = len,
            separators=self.seperators,
            add_start_index = True
        )

        chunks = []
        for doc_index, doc in enumerate(documents):
            split_docs = splitter.split_documents([doc])
            for chunk_index, chunk in enumerate(split_docs):
                meta= dict(chunk.metadata or {})
                meta.update({
                    "doc_index": doc_index,
                    "chunk_index": chunk_index,
                    "chunk_size": self.chunk_size,
                    "chunk_overlap": self.chunk_overlap,
                    "stategy": "Recursive"
                })

                chunks.append(Document(page_content=chunk.page_content.strip(), metadata=meta))
        return chunks