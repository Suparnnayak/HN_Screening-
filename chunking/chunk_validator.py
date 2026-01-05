# chunking/chunk_validator.py

from typing import List
from chunking.chunk_builder import Chunk


def validate_chunks(chunks: List[Chunk]) -> None:
    """
    Validates chunk integrity.
    Raises Exception if validation fails.
    """

    if len(chunks) != 5:
        raise ValueError(
            f"Expected 5 chunks, got {len(chunks)}"
        )

    required_metadata_fields = {
        "ppt_id",
        "team_name",
        "section",
        "week",
        "created_at"
    }

    seen_sections = set()

    for idx, chunk in enumerate(chunks):
        if not chunk.text:
            raise ValueError(f"Chunk {idx} has empty text")

        if not isinstance(chunk.metadata, dict):
            raise ValueError(f"Chunk {idx} metadata is invalid")

        missing_fields = required_metadata_fields - chunk.metadata.keys()
        if missing_fields:
            raise ValueError(
                f"Chunk {idx} missing metadata fields: {missing_fields}"
            )

        section = chunk.metadata["section"]
        if section in seen_sections:
            raise ValueError(
                f"Duplicate section detected: {section}"
            )
        seen_sections.add(section)

    if len(seen_sections) != 5:
        raise ValueError(
            f"Expected 5 unique sections, got {len(seen_sections)}"
        )
    print("All chunks validated successfully.")