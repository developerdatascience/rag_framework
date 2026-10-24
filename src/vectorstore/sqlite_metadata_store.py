import sqlite3
from typing import List, Dict, Any, Optional

class SQLiteMetadataStore:
    def __init__(self, db_path: str = "data/metadata.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                source_type TEXT,
                file_name TEXT,
                title TEXT,
                page INTEGER,
                doc_index INTEGER,
                chunk_index INTEGER,
                chunk_size INTEGER,
                chunk_overlap INTEGER,
                strategy TEXT,
                content TEXT,
                metadata_json TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS document_sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT UNIQUE,
                source_type TEXT,
                file_name TEXT,
                added_at TEXT
            )
        """)
        conn.commit()
        conn.close()

    def insert_document(self, doc: Dict[str, Any]) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            INSERT INTO documents (
                source, source_type, file_name, title, page, doc_index, chunk_index,
                chunk_size, chunk_overlap, strategy, content, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                doc.get("source"),
                doc.get("source_type"),
                doc.get("file_name"),
                doc.get("title"),
                doc.get("page"),
                doc.get("doc_index"),
                doc.get("chunk_index"),
                doc.get("chunk_size"),
                doc.get("chunk_overlap"),
                doc.get("strategy"),
                doc.get("content"),
                str(doc.get("metadata_json", {}))
            )
        )
        conn.commit()
        conn.close()

    def get_by_source(self, source: str) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT * FROM documents WHERE source = ? ORDER BY doc_index, chunk_index",
            (source,)
        ).fetchall()
        conn.close()
        return [self._row_to_dict(row) for row in rows]

    def _row_to_dict(self, row):
        keys = [
            "id", "source", "source_type", "file_name", "title", "page", "doc_index",
            "chunk_index", "chunk_size", "chunk_overlap", "strategy", "content", "metadata_json"
        ]
        return dict(zip(keys, row))