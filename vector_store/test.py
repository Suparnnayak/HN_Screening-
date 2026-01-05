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
from config.settings import EMBEDDING_MODEL_NAME

# Resolve path relative to repository root
pdf_path = (ROOT / "data" / "raw_ppts" / "sample.pdf").resolve()

pages = extract_text_from_pdf(pdf_path)
sections = map_text_to_sections(pages)

chunks = build_chunks(
    sections=sections,
    ppt_id="sample_001",
    team_name="FINNOVA",
    week=1
)
validate_chunks(chunks)

embedder = EmbeddingGenerator(EMBEDDING_MODEL_NAME)
embedded_chunks = embedder.embed_chunks(chunks)

# Initialize vector DB
client = ChromaClient()
collection = client.get_collection("hack_nocturne_2026")
store = VectorStore(collection)

store.add_embeddings(embedded_chunks)
client.persist()

# Test similarity search
query_embedding = embedder.embed_texts(
    ["student finance management app"]
)[0]

results = store.similarity_search(
    query_embedding=query_embedding,
    top_k=3,
    filters={"section": "idea_problem"}
)

print("Retrieved results:")
for r in results:
    print(r["metadata"], r["distance"])
