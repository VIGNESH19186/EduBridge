"""Format retrieved source metadata into student-facing citations."""
from typing import List, Dict


def format_citations(sources: List[Dict]) -> List[Dict]:
    return [
        {
            "title": s.get("title", "Unknown Source"),
            "section": s.get("section", ""),
            "source": s.get("source") or "Open Educational Resource",
        }
        for s in sources
    ]
