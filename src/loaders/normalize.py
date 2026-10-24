from typing import List, Dict, Any
from langchain_core.documents import Document

def normalize_docs(docs: List[Document], source: str, source_type: str) -> List[Document]:
    normalized = []
    for i, doc in enumerate(docs):
        page = doc.metadata.get("page", None)
        title = doc.metadata.get("title", None)
        file_name = doc.metadata.get("source", source)

        meta = {
            "source": source,
            "source_type": source_type,
            "file_name": file_name,
            "page": page,
            "title": title,
            "doc_index": i
        }

        meta.update(doc.metadata)
        normalized.append(
            Document(
                page_content=doc.page_content.strip(),
                metadata = meta)
        )
    return normalized