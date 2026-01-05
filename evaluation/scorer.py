# evaluation/scorer.py

from typing import Dict, List
from evaluation.prompts import (
    BASE_EVALUATION_PROMPT,
    CRITERION_INSTRUCTIONS,
    UNIQUENESS_PROMPT
)
from evaluation.retrieval_rules import RETRIEVAL_RULES
from config.settings import SCORE_WEIGHTS
import json


class Evaluator:
    """
    Evaluates a single PPT using RAG-based scoring.
    """

    def __init__(self, vector_store, embedder, llm_client):
        self.vector_store = vector_store
        self.embedder = embedder
        self.llm_client = llm_client

    def _retrieve_context(
        self,
        query_text: str,
        sections: List[str],
        filters: Dict,
        top_k: int = 5
    ) -> str:
        query_embedding = self.embedder.embed_texts([query_text])[0]

        retrieved = self.vector_store.similarity_search(
            query_embedding=query_embedding,
            top_k=top_k,
            filters=filters
        )

        texts = []
        for item in retrieved:
            if item["metadata"]["section"] in sections:
                texts.append(item["text"])

        return "\n\n".join(texts)

    def score_criterion(
        self,
        criterion_name: str,
        ppt_id: str
    ) -> Dict:
        rule = RETRIEVAL_RULES[criterion_name]

        filters = {"ppt_id": ppt_id}
        if rule["cross_ppt"]:
            filters = {"ppt_id": {"$ne": ppt_id}}

        context = self._retrieve_context(
            query_text=criterion_name.replace("_", " "),
            sections=rule["sections"],
            filters=filters
        )

        prompt = BASE_EVALUATION_PROMPT.format(
            context=context,
            criterion=CRITERION_INSTRUCTIONS[criterion_name]
        )

        response = self.llm_client.generate(prompt)

        return json.loads(response)

    def score_uniqueness(
        self,
        ppt_id: str,
        idea_text: str
    ) -> Dict:
        rule = RETRIEVAL_RULES["uniqueness"]

        query_embedding = self.embedder.embed_texts([idea_text])[0]

        similar_items = self.vector_store.similarity_search(
            query_embedding=query_embedding,
            top_k=5,
            filters={"ppt_id": {"$ne": ppt_id}}
        )

        similar_texts = [
            item["text"] for item in similar_items
        ]

        prompt = UNIQUENESS_PROMPT.format(
            current_idea=idea_text,
            similar_ideas="\n\n".join(similar_texts)
        )

        response = self.llm_client.generate(prompt)

        return json.loads(response)

    def evaluate_ppt(
        self,
        ppt_id: str,
        idea_text: str
    ) -> Dict:
        scores = {}

        total_score = 0

        for criterion in [
            "problem_clarity",
            "solution_quality",
            "technical_feasibility",
            "team_capability"
        ]:
            result = self.score_criterion(criterion, ppt_id)
            scores[criterion] = result
            total_score += result["score"]

        uniqueness_result = self.score_uniqueness(ppt_id, idea_text)
        scores["uniqueness"] = uniqueness_result
        total_score += uniqueness_result["score"]

        scores["total_score"] = min(total_score, 100)

        return scores
