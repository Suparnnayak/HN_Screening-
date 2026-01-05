# pipeline/batch_runner.py

from pathlib import Path
from pipeline import run_pipeline


def run_batch(
    pdf_folder: Path,
    week: int,
    hackathon_id: str
):
    """
    Runs evaluation pipeline for all PDFs in a folder.
    """

    pdf_files = list(pdf_folder.glob("*.pdf"))

    if not pdf_files:
        raise ValueError("No PDF files found in folder")

    print(f"Found {len(pdf_files)} PDFs. Starting batch processing...\n")

    for idx, pdf_path in enumerate(pdf_files, start=1):
        ppt_id = f"ppt_{week}_{idx}"
        team_name = pdf_path.stem  # filename as team_name

        print(f"[{idx}/{len(pdf_files)}] Processing: {team_name}")

        try:
            run_pipeline(
                pdf_path=pdf_path,
                ppt_id=ppt_id,
                team_name=team_name,
                week=week,
                hackathon_id=hackathon_id
            )
        except Exception as e:
            print(f"❌ Failed for {team_name}: {e}")

    print("\nBatch processing completed.")
