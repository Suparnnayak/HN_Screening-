import sys
from pathlib import Path

# Ensure repository root is on sys.path so sibling packages can be imported
ROOT = Path(__file__).parent.parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ingestion import extract_text_from_pdf, map_text_to_sections
from chunking import build_chunks, validate_chunks
from embeddings import EmbeddingGenerator
from vector_store import ChromaClient, VectorStore
from uniqueness import compute_internal_similarity, adjust_uniqueness_score
from config.settings import EMBEDDING_MODEL_NAME

# Resolve path relative to repository root
pdf_path = (ROOT / "data" / "raw_ppts" / "sample.pdf").resolve()

pages = extract_text_from_pdf(pdf_path)
sections = map_text_to_sections(pages)

chunks = build_chunks(
    sections=sections,
    ppt_id="sample_002",
    team_name="FINNOVA",
    week=1
)
validate_chunks(chunks)

idea_text = sections["idea_problem"]

embedder = EmbeddingGenerator(EMBEDDING_MODEL_NAME)

client = ChromaClient()
collection = client.get_collection("hack_nocturne_2026")
store = VectorStore(collection)

similarity_stats = compute_internal_similarity(
    vector_store=store,
    embedder=embedder,
    ppt_id="sample_002",
    idea_text=idea_text
)

adjusted = adjust_uniqueness_score(
    base_score=25,
    similarity_stats=similarity_stats
)

print(adjusted)
