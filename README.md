hackathon_ai_evaluator/
│
├── data/
│   ├── raw_ppts/              # Uploaded PDFs/PPTs
│   ├── extracted_text/        # Debug: extracted text (optional)
│   ├── embeddings_cache/      # Optional: cached embeddings
│
├── ingestion/
│   ├── __init__.py
│   ├── pdf_parser.py          # pdfplumber / PyMuPDF logic
│   ├── ppt_parser.py          # python-pptx logic (if PPT)
│   ├── template_mapper.py     # maps content to 5 sections
│
├── chunking/
│   ├── __init__.py
│   ├── chunk_builder.py       # builds 5 chunks
│   ├── chunk_validator.py     # ensures all sections exist
│
├── embeddings/
│   ├── __init__.py
│   ├── embedder.py            # SentenceTransformer wrapper
│
├── vector_store/
│   ├── __init__.py
│   ├── chroma_client.py       # ChromaDB setup
│   ├── store.py               # add/search logic
│
├── evaluation/
│   ├── __init__.py
│   ├── prompts.py             # ALL frozen prompts live here
│   ├── scorer.py              # scoring out of 100
│   ├── retrieval_rules.py     # what to retrieve for what
│
├── uniqueness/
│   ├── __init__.py
│   ├── internal_similarity.py # compare against past PPTs
│   ├── uniqueness_adjuster.py # apply penalties/bonuses
│
├── llm/
│   ├── __init__.py
│   ├── ollama_client.py       # local LLM calls
│
├── output/
│   ├── __init__.py
│   ├── excel_writer.py        # append results
│   ├── ranking.py             # top-300 logic
│
├── pipeline/
│   ├── __init__.py
│   ├── run_pipeline.py        # orchestrates everything
│
├── config/
│   ├── settings.py            # paths, model names, constants
│
├── main.py                    # entry point
├── requirements.txt
├── README.md
