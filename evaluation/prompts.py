# evaluation/prompts.py

BASE_EVALUATION_PROMPT = """
You are an AI evaluator. Respond ONLY with valid JSON. Do not include any other text.

Evaluation rules:
- Be conservative and objective.
- Do NOT assume missing information.
- Penalize vague, generic, or marketing-style language.
- Judge ONLY based on the provided context.
- Do NOT add external knowledge.

Context:
{context}

Evaluation Criterion:
{criterion}

Scoring rules:
- The score must be an integer within the specified range.
- Respond ONLY with the JSON object below. No preamble, no explanation.

If the context is insufficient to evaluate, return exactly:
{{"score": 0, "reason": "Insufficient information provided."}}

RESPOND ONLY WITH THIS JSON (nothing else):
{{
  "score": <integer>,
  "reason": "<short, factual justification>"
}}
"""


CRITERION_INSTRUCTIONS = {
    "problem_clarity": """
Evaluate how clearly the problem is defined.
Reward:
- Clear articulation of the problem
- Well-defined scope
- Relevance to real users

Penalize:
- Vague descriptions
- Buzzwords without explanation

Score range: 0–20.
""",

    "solution_quality": """
Evaluate the proposed solution approach.
Reward:
- Logical flow
- Clear steps or methodology
- Practical feasibility

Penalize:
- Hand-wavy descriptions
- Missing explanation of how the solution works

Score range: 0–15.
""",

    "technical_feasibility": """
Evaluate technical feasibility based on the described tech stack.
Reward:
- Appropriate and realistic technology choices
- Alignment between problem and tools

Penalize:
- Missing tech stack
- Overly generic or unrealistic claims

Score range: 0–15.
""",

    "team_capability": """
Evaluate the team's capability to execute the idea.
Reward:
- Relevant skills
- Clear roles or experience
- Motivation aligned with the problem

Penalize:
- Generic team descriptions
- No evidence of execution readiness

Score range: 0–10.
"""
}


UNIQUENESS_PROMPT = """
You are evaluating the uniqueness of a hackathon idea. Respond ONLY with valid JSON. Do not include any other text.

Evaluation rules:
- Do NOT penalize common problem statements.
- Focus on solution approach and differentiation.
- Do NOT assume plagiarism.
- Do NOT auto-reject ideas.
- Be conservative and fair.

Current Idea:
{current_idea}

Similar Ideas from other submissions:
{similar_ideas}

RESPOND ONLY WITH THIS JSON (nothing else):
{{
  "novelty_category": "near-duplicate | common | novel | highly-original",
  "score": <integer between 0 and 40>,
  "reason": "<short factual justification>"
}}
"""
