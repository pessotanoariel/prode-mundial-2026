from pathlib import Path
from datetime import datetime

import pandas as pd


ELO_TSV_URL = "https://www.eloratings.net/World.tsv"

RAW_OUTPUT_PATH = Path("data/raw/elo_rankings.csv")


def download_elo_rankings() -> pd.DataFrame:
    """
    Download world football Elo rankings from TSV source.
    """

    column_names = [
        "rank",
        "team",
        "country_code",
        "rating",
        "average_rank",
        "average_rating",
        "1_year_rank",
        "1_year_rating",
        "3_year_rank",
        "3_year_rating",
        "rank_change",
        "rating_change",
        "home_rank_change",
        "home_rating_change",
        "away_rank_change",
        "away_rating_change",
        "win_rank_change",
        "win_rating_change",
        "loss_rank_change",
        "loss_rating_change",
        "goal_rank_change",
        "goal_rating_change",
        "matches_total",
        "matches_home",
        "matches_away",
        "matches_neutral",
        "wins",
        "losses",
        "draws",
        "goals_for",
        "goals_against"
    ]

    df = pd.read_csv(
        ELO_TSV_URL,
        sep="\t",
        header=None,
        names=column_names
    )

    df["extracted_at"] = datetime.now().isoformat(timespec="seconds")
    df["source"] = ELO_TSV_URL

    return df


def main() -> None:

    RAW_OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df = download_elo_rankings()

    df.to_csv(
        RAW_OUTPUT_PATH,
        index=False,
        encoding="utf-8"
    )

    print(f"\nOK - Elo rankings saved to {RAW_OUTPUT_PATH}\n")

    print(df.head(10))

    print("\nColumns:")
    print(df.columns.tolist())


if __name__ == "__main__":
    main()