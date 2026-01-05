# main.py

from pathlib import Path
from pipeline.batch_runner import run_batch


def main():
    pdf_folder = Path("data/raw_ppts")
    week = 1
    hackathon_id = "hack_nocturne_2026"

    run_batch(
        pdf_folder=pdf_folder,
        week=week,
        hackathon_id=hackathon_id
    )


if __name__ == "__main__":
    main()
