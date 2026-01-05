import sys
from pathlib import Path

# Ensure repository root is on sys.path so sibling packages can be imported
ROOT = Path(__file__).parent.parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ingestion import extract_text_from_pdf, map_text_to_sections
from chunking import build_chunks, validate_chunks

# Resolve path relative to repository root
pdf_path = (ROOT / "data" / "raw_ppts" / "sample.pdf").resolve()

pages = extract_text_from_pdf(pdf_path)
sections = map_text_to_sections(pages)

chunks = build_chunks(
    sections=sections,
    ppt_id="sample_ppt_001",
    team_name="FINNOVA",
    week=1
)

validate_chunks(chunks)

for c in chunks:
    print("\n---", c.metadata["section"].upper(), "---")
    print(c.text)
