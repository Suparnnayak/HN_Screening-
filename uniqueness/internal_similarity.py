# uniqueness/internal_similarity.py

from typing import List, Dict, Any
import numpy as np


def compute_internal_similarity(
    vector_store,
    embedder,
    ppt_id: str,
    idea_text: str,
    top_k: int = 5
) -> Dict[str, Any]:
    """
    Computes semantic similarity of the current idea
    against past submissions (excluding itself).

    Returns similarity statistics, not decisions.
    """

    # Embed current idea
    query_embedding = embedder.embed_texts([idea_text])[0]

    # Build a Chroma-compatible filter: top-level must have exactly one operator
    filters = {
        "$and": [
            {"ppt_id": {"$ne": ppt_id}},
            {"section": "idea_problem"}
        ]
    }

    # Retrieve similar past ideas
    results = vector_store.similarity_search(
        query_embedding=query_embedding,
        top_k=top_k,
        filters=filters
    )


    if not results:
        return {
            "max_similarity": 0.0,
            "avg_similarity": 0.0,
            "matched_count": 0,
            "raw_results": []
        }

    # Convert Chroma distances to similarity scores
    # (distance is cosine distance since embeddings are normalized)
    similarities = [1 - r["distance"] for r in results]

    return {
        "max_similarity": float(np.max(similarities)),
        "avg_similarity": float(np.mean(similarities)),
        "matched_count": len(similarities),
        "raw_results": results
    }
