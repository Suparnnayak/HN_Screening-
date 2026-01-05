# uniqueness/uniqueness_adjuster.py

from typing import Dict, Any


def adjust_uniqueness_score(
    base_score: int,
    similarity_stats: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Adjusts uniqueness score based on internal similarity signals.
    """

    max_sim = similarity_stats["max_similarity"]
    adjustment = 0
    reason = "Idea appears sufficiently distinct."

    if max_sim >= 0.90:
        adjustment = -10
        reason = "Idea is very similar to existing submissions."
    elif max_sim >= 0.80:
        adjustment = -6
        reason = "Idea is a common pattern seen in multiple submissions."
    elif max_sim >= 0.70:
        adjustment = -3
        reason = "Idea overlaps with known approaches."
    elif max_sim < 0.55:
        adjustment = +3
        reason = "Idea shows high novelty compared to past submissions."

    adjusted_score = max(0, min(base_score + adjustment, 40))

    return {
        "base_score": base_score,
        "adjustment": adjustment,
        "final_score": adjusted_score,
        "reason": reason,
        "similarity_stats": similarity_stats
    }
