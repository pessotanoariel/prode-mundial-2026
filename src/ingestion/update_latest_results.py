from pathlib import Path
from datetime import datetime

import pandas as pd


LATEST_TSV_URL = "https://www.eloratings.net/latest.tsv"
RAW_OUTPUT_PATH = Path("data/raw/latest_results.csv")


def download_latest_results() -> pd.DataFrame:
    column_names = [
        "year",
        "month",
        "day",
        "team_1_code",
        "team_2_code",
        "team_1_goals",
        "team_2_goals",
        "tournament_code",
        "host_code",
        "team_1_rating_change",
        "team_1_rating",
        "team_2_rating",
        "team_1_rank_change",
        "team_2_rank_change",
        "team_1_rank",
        "team_2_rank",
    ]

    df = pd.read_csv(
        LATEST_TSV_URL,
        sep="\t",
        header=None,
        names=column_names,
    )

    df["match_date"] = pd.to_datetime(
        df[["year", "month", "day"]]
    )

    df["extracted_at"] = datetime.now().isoformat(timespec="seconds")
    df["source"] = LATEST_TSV_URL

    return df


def main() -> None:
    RAW_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = download_latest_results()

    df.to_csv(RAW_OUTPUT_PATH, index=False, encoding="utf-8")

    print(f"\nOK - Latest results saved to {RAW_OUTPUT_PATH}\n")
    print(df.head(10))
    print("\nColumns:")
    print(df.columns.tolist())


if __name__ == "__main__":
    main()