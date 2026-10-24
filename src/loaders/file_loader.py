from langchain_community.document_loaders import (TextLoader, 
WebBaseLoader, BSHTMLLoader, PyMuPDFLoader, UnstructuredWordDocumentLoader, UnstructuredMarkdownLoader)
from pathlib import Path
from typing import List
from langchain_core.documents import Document

from src.loaders.base_loader import BaseLoader
from src.loaders.normalize import normalize_docs


class FileLoader(BaseLoader):
    def load(self, source: str) -> List[Document]:
        path = Path(source)

        if not path.exists():
            raise ValueError(f"Soure file not found: {source}")

        suffix = path.suffix.lower()

        if suffix == ".txt":
            loader=TextLoader(str(path), encoding="utf-8")
            docs = loader.load()

        elif suffix == ".md":
            loader = UnstructuredMarkdownLoader(str(path), mode="elements")
            docs = loader.load()

        elif suffix == '.docx':
            loader = UnstructuredWordDocumentLoader(str(path))
            docs = loader.load()

        elif suffix == '.pdf':
            loader = PyMuPDFLoader(str(path))
            docs = loader.load()

        elif suffix in ('.html', '.htm'):
            loader = BSHTMLLoader(str(path), open_encoding="utf-8")
            docs = loader.load()

        else:
            raise ValueError(f"Unsupported file type: {suffix}")

        return normalize_docs(docs=docs, source=source, source_type='file')