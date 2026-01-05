# output/excel_writer.py

import pandas as pd
from pathlib import Path
from typing import Dict
from config.settings import RESULTS_FILE


def append_result(
    ppt_id: str,
    team_name: str,
    week: int,
    scores: Dict
):
    """
    Appends a single PPT evaluation result to Excel.
    """

    row = {
        "ppt_id": ppt_id,
        "team_name": team_name,
        "week": week,
        "problem_clarity": scores["problem_clarity"]["score"],
        "solution_quality": scores["solution_quality"]["score"],
        "technical_feasibility": scores["technical_feasibility"]["score"],
        "team_capability": scores["team_capability"]["score"],
        "uniqueness": scores["uniqueness"]["final_score"],
        "total_score": scores["total_score"],
        "remarks": scores["uniqueness"]["reason"]
    }

    df_new = pd.DataFrame([row])

    if RESULTS_FILE.exists():
        df_existing = pd.read_excel(RESULTS_FILE)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_excel(RESULTS_FILE, index=False)
