from typing import List, Optional, Dict, Any
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from src.vectorstore.base_vectorstore import BaseVectorStore

class FAISSVectorStore(BaseVectorStore):
    def __init__(self, embedding_model, index_path: str | None = None):
        self.embedding_model = embedding_model
        self.index_path = index_path
        self.store = None


    def add_documents(self, documents: List[Document]) -> None:
        if self.store is None:
            self.store = FAISS.from_documents(documents=documents, embedding=self.embedding_model)
        else:
            self.store.add_documents(documents=documents)


    def similarity_search(self, 
                          query: str,
                          k: int = 5,
                          filter: Optional[Dict[str, Any]] = None
                          ) -> List[Document]:
        if self.store is None:
            raise ValueError(f"Vectore store is not initialized. Add documents before searching")

        if filter:
            # FAISS itself doesn't do metadata filtering natively in the same way
            # so we handle it with a post-filter over results.
            results = self.store.similarity_search(query=query, k=k * 3)
            return [doc for doc in results if self._matches_filter(doc.metadata, filter)][:k]

        return self.store.similarity_search(query=query, k=k)


    def _matches_filter(self, metadata: Dict[str, Any], filter_dict: Dict[str, Any]) -> bool:
        for key, expected in filter_dict.items():
            if metadata.get(key) != expected:
                return False
        return True

    def save_local(self, path: str) ->None:
        if self.store is None:
            raise ValueError("No FAISS index to save")
        self.store.save_local(path)
        self.index_path = path


    def load_local(self, path: str) -> None:
        self.store = FAISS.load_local(path, self.embedding_model, allow_dangerous_deserialization=True)
        self.index_path = path