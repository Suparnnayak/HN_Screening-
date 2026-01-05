# pipeline/run_pipeline.py

from pathlib import Path
from ingestion import extract_text_from_pdf, map_text_to_sections
from chunking import build_chunks, validate_chunks
from embeddings import EmbeddingGenerator
from vector_store import ChromaClient, VectorStore
from uniqueness import compute_internal_similarity, adjust_uniqueness_score
from evaluation import Evaluator
from llm import OllamaClient
from output import append_result
from config.settings import EMBEDDING_MODEL_NAME


def run_pipeline(
    pdf_path: Path,
    ppt_id: str,
    team_name: str,
    week: int,
    hackathon_id: str
):
    """
    Runs end-to-end evaluation for a single PPT.
    """

    # 1. Ingestion
    pages = extract_text_from_pdf(pdf_path)
    sections = map_text_to_sections(pages)

    # 2. Chunking
    chunks = build_chunks(
        sections=sections,
        ppt_id=ppt_id,
        team_name=team_name,
        week=week
    )
    validate_chunks(chunks)

    # 3. Embeddings
    embedder = EmbeddingGenerator(EMBEDDING_MODEL_NAME)
    embedded_chunks = embedder.embed_chunks(chunks)

    # 4. Vector store
    chroma = ChromaClient()
    collection = chroma.get_collection(hackathon_id)
    store = VectorStore(collection)
    store.add_embeddings(embedded_chunks)
    chroma.persist()

    # 5. Internal uniqueness (pre-LLM)
    idea_text = sections["idea_problem"]
    similarity_stats = compute_internal_similarity(
        vector_store=store,
        embedder=embedder,
        ppt_id=ppt_id,
        idea_text=idea_text
    )

    # 6. LLM evaluation
    llm_client = OllamaClient()
    evaluator = Evaluator(
        vector_store=store,
        embedder=embedder,
        llm_client=llm_client
    )

    scores = evaluator.evaluate_ppt(
        ppt_id=ppt_id,
        idea_text=idea_text
    )

    # 7. Adjust uniqueness score
    adjusted_uniqueness = adjust_uniqueness_score(
        base_score=scores["uniqueness"]["score"],
        similarity_stats=similarity_stats
    )
    scores["uniqueness"] = adjusted_uniqueness

    # Recalculate total
    scores["total_score"] = (
        scores["problem_clarity"]["score"] +
        scores["solution_quality"]["score"] +
        scores["technical_feasibility"]["score"] +
        scores["team_capability"]["score"] +
        scores["uniqueness"]["final_score"]
    )

    # 8. Output
    append_result(
        ppt_id=ppt_id,
        team_name=team_name,
        week=week,
        scores=scores
    )

    return scores
