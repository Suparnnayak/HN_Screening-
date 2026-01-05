# config/settings.py

from pathlib import Path

# =========================
# PROJECT ROOT
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# DATA DIRECTORIES
# =========================
DATA_DIR = BASE_DIR / "data"
RAW_PPTS_DIR = DATA_DIR / "raw_ppts"
EXTRACTED_TEXT_DIR = DATA_DIR / "extracted_text"
EMBEDDINGS_CACHE_DIR = DATA_DIR / "embeddings_cache"

# Ensure directories exist
for directory in [
    DATA_DIR,
    RAW_PPTS_DIR,
    EXTRACTED_TEXT_DIR,
    EMBEDDINGS_CACHE_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)

# =========================
# VECTOR DATABASE (Chroma)
# =========================
CHROMA_PERSIST_DIR = BASE_DIR / "chroma_db"
CHROMA_COLLECTION_NAME = "hackathon_ppts"

# =========================
# EMBEDDING MODEL
# =========================
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# =========================
# LLM (Ollama)
# =========================
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL_NAME = "llama3"

# =========================
# CHUNKING CONFIG
# =========================
REQUIRED_SECTIONS = [
    "idea_problem",
    "solution_approach",
    "uniqueness_claim",
    "tech_stack",
    "team_capability",
]

# =========================
# SCORING CONFIG (OUT OF 100)
# =========================
SCORE_WEIGHTS = {
    "uniqueness": 40,
    "problem_clarity": 20,
    "solution_quality": 15,
    "technical_feasibility": 15,
    "team_capability": 10,
}

TOTAL_SCORE = 100

# =========================
# RETRIEVAL CONFIG
# =========================
TOP_K_RETRIEVAL = 5

# =========================
# EXCEL OUTPUT
# =========================
RESULTS_FILE = BASE_DIR / "results.xlsx"

# =========================
# SAFETY & LIMITS
# =========================
MAX_LLM_RETRIES = 2
LLM_TIMEOUT_SECONDS = 120
