# output/ranking.py

import pandas as pd
from config.settings import RESULTS_FILE
from typing import Optional


def get_top_teams(top_n: int = 300) -> pd.DataFrame:
    """
    Returns top-N teams based on total_score.
    """

    if not RESULTS_FILE.exists():
        raise FileNotFoundError("Results file not found")

    df = pd.read_excel(RESULTS_FILE)

    df_sorted = df.sort_values(
        by="total_score",
        ascending=False
    )

    return df_sorted.head(top_n)
