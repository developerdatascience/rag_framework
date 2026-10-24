from typing import List, Any, Optional, Dict
from langchain_core.documents import Document

from src.retrieval.base_retriever import BaseRetriever

class SemanticRetriever(BaseRetriever):
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore

    def retrieve(self, 
                 query: str, 
                 k: int,
                 filters: Optional[Dict[str, Any]] = None
                 ) -> List[Document]:

        return self.vectorstore.similarity_search(query=query, k=k, filter=filters)