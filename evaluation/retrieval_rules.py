# evaluation/retrieval_rules.py

RETRIEVAL_RULES = {
    "problem_clarity": {
        "sections": ["idea_problem"],
        "cross_ppt": False
    },
    "solution_quality": {
        "sections": ["solution_approach"],
        "cross_ppt": False
    },
    "technical_feasibility": {
        "sections": ["tech_stack"],
        "cross_ppt": False
    },
    "team_capability": {
        "sections": ["team_capability"],
        "cross_ppt": False
    },
    "uniqueness": {
        "sections": ["idea_problem", "solution_approach"],
        "cross_ppt": True
    }
}
