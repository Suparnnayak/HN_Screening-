# chunking/chunk_builder.py

from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Chunk:
    text: str
    metadata: Dict


def build_chunks(
    sections: Dict[str, str],
    ppt_id: str,
    team_name: str,
    week: int
) -> List[Chunk]:
    """
    Builds exactly 5 chunks from mapped template sections.
    Missing sections are explicitly marked.
    """

    REQUIRED_SECTIONS = [
        "idea_problem",
        "solution_approach",
        "uniqueness_claim",
        "tech_stack",
        "team_capability",
    ]

    chunks: List[Chunk] = []

    for section in REQUIRED_SECTIONS:
        raw_text = sections.get(section, "").strip()

        if not raw_text:
            chunk_text = "[SECTION NOT PROVIDED BY TEAM]"
        else:
            chunk_text = normalize_text(raw_text)

        metadata = {
            "ppt_id": ppt_id,
            "team_name": team_name,
            "section": section,
            "week": week,
            "created_at": datetime.utcnow().isoformat()
        }

        chunks.append(
            Chunk(
                text=chunk_text,
                metadata=metadata
            )
        )

    return chunks


def normalize_text(text: str) -> str:
    """
    Minimal normalization:
    - Remove excessive newlines
    - Preserve original wording
    """

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)
