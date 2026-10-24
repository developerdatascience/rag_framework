# modules/loaders/registry.py
from pathlib import Path
from typing import List
from langchain_core.documents import Document

from src.loaders.file_loader import FileLoader
from src.loaders.folder_loader import FolderLoader
from src.loaders.web_loader import WebLoader

class LoaderRegistry:
    def __init__(self):
        self.file_loader = FileLoader()
        self.folder_loader = FolderLoader()
        self.web_loader = WebLoader()

    def load(self, source: str) -> List[Document]:
        # detect if source is URL
        if source.startswith(("http://", "https://")):
            return self.web_loader.load(source)

        path = Path(source)
        if path.exists() and path.is_dir():
            return self.folder_loader.load(source)

        if path.exists() and path.is_file():
            return self.file_loader.load(source)

        raise ValueError(f"Unsupported source or path: {source}")