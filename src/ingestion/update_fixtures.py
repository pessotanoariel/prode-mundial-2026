from pathlib import Path
from datetime import datetime

import pandas as pd


FIXTURES_TSV_URL = "https://www.eloratings.net/fixtures.tsv"
RAW_OUTPUT_PATH = Path("data/raw/fixtures.csv")


def download_fixtures() -> pd.DataFrame:
    column_names = [
        "year",
        "month",
        "day",
        "team_1_code",
        "team_2_code",
        "tournament_code",
        "host_code",
        "team_1_rank",
        "team_2_rank",
        "team_1_rating",
        "team_2_rating",
        "team_1_win_expectancy",
        "draw_points_exchange",
        "team_1_win_by_1_points",
        "team_2_win_by_1_points",
        "team_1_win_by_2_points",
        "team_2_win_by_2_points",
        "team_1_win_by_3_points",
        "team_2_win_by_3_points",
        "team_1_win_by_4_points",
        "team_2_win_by_4_points",
        "team_1_win_by_5_points",
        "team_2_win_by_5_points",
    ]

    df = pd.read_csv(
        FIXTURES_TSV_URL,
        sep="\t",
        header=None,
        names=column_names,
    )

    df["match_date"] = pd.to_datetime(
        dict(
            year=df["year"],
            month=df["month"],
            day=df["day"].replace(0, 1)
        ),
        errors="coerce"
    )

    df["extracted_at"] = datetime.now().isoformat(timespec="seconds")
    df["source"] = FIXTURES_TSV_URL

    return df


def main() -> None:
    RAW_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = download_fixtures()

    df.to_csv(RAW_OUTPUT_PATH, index=False, encoding="utf-8")

    print(f"\nOK - Fixtures saved to {RAW_OUTPUT_PATH}\n")
    print(df.head(10))
    print("\nColumns:")
    print(df.columns.tolist())


if __name__ == "__main__":
    main()