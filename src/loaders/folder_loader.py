from pathlib import Path
from langchain_core.documents import Document
from typing import List, Any, Dict

from src.loaders.file_loader import FileLoader


class FolderLoader:
    def __init__(self, allowed_extensions = None):
        self.allowed_extensions = allowed_extensions or {'.txt', '.md', '.pdf', '.docx', '.html', '.htm'}
        self.file_loader = FileLoader()


    def load(self, folder_path: str) -> List[Document]:
        folder = Path(folder_path)

        if not folder.exists() and not folder.is_dir():
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        docs: List[Document] = []
        for file_path in sorted(folder.rglob("*")):
            if file_path.is_file() and file_path.suffix.lower() in self.allowed_extensions:
                docs.extend(self.file_loader.load(str(file_path)))

        return docs
