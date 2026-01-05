# ingestion/pdf_parser.py

import pdfplumber
from pathlib import Path
from typing import Dict, List
import logging

logging.getLogger("pdfminer").setLevel(logging.ERROR)

def extract_text_from_pdf(pdf_path: Path) -> Dict[int, str]:
    """
    Extracts text from a PDF file page by page.

    Returns:
        {
            page_number (1-based): extracted_text
        }
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    extracted_pages: Dict[int, str] = {}

    with pdfplumber.open(pdf_path) as pdf:
        for idx, page in enumerate(pdf.pages):
            page_number = idx + 1
            text = page.extract_text()

            if text:
                cleaned_text = text.strip()
            else:
                cleaned_text = ""

            extracted_pages[page_number] = cleaned_text

    return extracted_pages
