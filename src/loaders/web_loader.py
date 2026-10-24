from langchain_community.document_loaders import WebBaseLoader
from src.loaders.normalize import normalize_docs
from src.loaders.base_loader import BaseLoader

from langchain_core.documents import Document
from typing import List

class WebLoader(BaseLoader):
    def load(self, source: str) -> List[Document]:
        loader = WebBaseLoader(source)
        docs = loader.load()
        return normalize_docs(docs, source, "web")