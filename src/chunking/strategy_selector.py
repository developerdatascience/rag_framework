from dataclasses import dataclass
from typing import List, Dict, Any

from langchain_core.documents import Document

@dataclass
class StrategyCandidate:
    name: str
    chunk_size: int
    chunk_overlap: int
    score: float = 0.0

class StrategySelector:
    def __init__(self, default_strategy: str = "recursive"):
        self.default_strategy = default_strategy

    def _estimate_doc_profile(self, documents: List[Document]) -> Dict[str, Any]:
        total_chars = sum(len(doc.page_content or "") for doc in documents)
        avg_chars = total_chars / max(1, len(documents))
        text_types = []

        for doc in documents:
            text = (doc.page_content or "").lower()
            if "\n\n" in text or "# " in text or "## " in text:
                text_types.append("structured")
            elif "```" in text:
                text_types.append("code")
            elif len(text) > 10000:
                text_types.append("long_form")
            else:
                text_types.append("general")

        primary_type = max(set(text_types), key=text_types.count)

        return {
            "total_chars": total_chars,
            "avg_chars": avg_chars,
            "primary_type": primary_type,
            "num_docs": len(documents),
        }

    def _build_candidates(self, profile: Dict[str, Any]) -> List[StrategyCandidate]:
        total_chars = profile["total_chars"]
        primary_type = profile["primary_type"]

        candidates = []

        if total_chars < 5000:
            candidates.append(StrategyCandidate("fixed_size", 500, 80))
            candidates.append(StrategyCandidate("recursive", 600, 100))
            candidates.append(StrategyCandidate("semantic", 700, 80))
        elif total_chars < 20000:
            candidates.append(StrategyCandidate("recursive", 800, 120))
            candidates.append(StrategyCandidate("fixed_size", 700, 100))
            candidates.append(StrategyCandidate("semantic", 900, 120))
        else:
            candidates.append(StrategyCandidate("semantic", 1200, 200))
            candidates.append(StrategyCandidate("recursive", 1000, 180))
            candidates.append(StrategyCandidate("fixed_size", 800, 120))

        # Adjust based on content type
        for c in candidates:
            if primary_type == "structured" and c.name == "recursive":
                c.score += 25
            if primary_type == "code" and c.name == "recursive":
                c.score += 20
            if primary_type == "long_form" and c.name == "semantic":
                c.score += 30
            if primary_type == "general" and c.name == "fixed_size":
                c.score += 10

        return candidates

    def select(self, documents: List[Document]) -> StrategyCandidate:
        if not documents:
            return StrategyCandidate(self.default_strategy, 800, 120, 0.0)

        profile = self._estimate_doc_profile(documents)
        candidates = self._build_candidates(profile)

        # Add simple quality heuristic based on chunk size vs document size
        for c in candidates:
            relative = c.chunk_size / max(1, profile["avg_chars"])
            if relative > 0.9:
                c.score -= 10
            if c.chunk_overlap > c.chunk_size * 0.35:
                c.score -= 8

        best = max(candidates, key=lambda x: x.score)
        return best