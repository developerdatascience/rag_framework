from typing import List
from langchain_experimental.text_splitter import SemanticChunker
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from src.chunking.base_chunker import BaseChunker
import os
from dotenv import load_dotenv

load_dotenv()


class SemanticChunkerWrapper(BaseChunker):
    def __init__(self, 
                 chunk_size: int = 1000, 
                 chunk_overlap: int = 150,
                 embeddings=None,
                 **kwargs) -> None:
        super().__init__(chunk_size=chunk_size, chunk_overlap=chunk_overlap, **kwargs)
        self.embeddings = embeddings or OpenAIEmbeddings(model=os.getenv("MODEL", ""),
                                                         base_url=os.getenv("BASE_URL", None),
                                                         api_key=os.getenv("OPENAI_API_KEY", None)
                                                         )

        def split(self, documents: List[Document]) -> List[Document]:
            splitter = SemanticChunker(
                embeddings=self.embeddings,
                breakpoint_threshold_type="percentile",
                breakpoint_threshold_amount=85,
                min_chunk_size=self.chunk_size // 2,
                max_chunk_size=self.chunk_size)

            chunks = []
            for doc_index, doc in enumerate(documents):
                semantic_chunks = splitter.split_text(doc.page_content)
                for chunk_index, text in enumerate(semantic_chunks):
                    meta = dict(doc.metadata or {})
                    meta.update({
                        "doc_index": doc_index,
                        "chunk_index": chunk_index,
                        "chunk_size": self.chunk_size,
                        "chunk_overlap": self.chunk_overlap,
                        "strategy": "semantic",
                    })
                    chunks.append(Document(page_content=text.strip(), metadata=meta))
            return chunks