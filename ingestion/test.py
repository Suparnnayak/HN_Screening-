from pathlib import Path
from pdf_parser import extract_text_from_pdf
from template_mapper import map_text_to_sections

# Resolve path relative to the repository root (two levels up from this file)
pdf_path = (Path(__file__).parent.parent / "data" / "raw_ppts" / "sample.pdf").resolve()

pages = extract_text_from_pdf(pdf_path)
sections = map_text_to_sections(pages)

for k, v in sections.items():
    print(f"\n--- {k.upper()} ---")
    print(v[:500])
