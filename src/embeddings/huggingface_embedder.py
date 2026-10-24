from typing import List
from langchain_huggingface import HuggingFaceEmbeddings

from src.embeddings.base_embedder import BaseEmbedder

class HuggingFaceEmbedder(BaseEmbedder):
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        **kwargs
    ):
        self.model = HuggingFaceEmbeddings(model_name=model_name, **kwargs)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.model.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        return self.model.embed_query(text)