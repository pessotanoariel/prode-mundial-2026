from pathlib import Path
from datetime import datetime

import pandas as pd


TEAMS_TSV_URL = "https://www.eloratings.net/en.teams.tsv"

RAW_OUTPUT_PATH = Path("data/raw/teams_lookup.csv")


def download_teams_lookup() -> pd.DataFrame:

    df = pd.read_csv(
        TEAMS_TSV_URL,
        sep="\t",
        header=None,
        usecols=[0, 1],
        engine="python"
    )

    df.columns = [
        "country_code",
        "team_name"
    ]

    df["extracted_at"] = datetime.now().isoformat(timespec="seconds")
    df["source"] = TEAMS_TSV_URL

    return df


def main() -> None:

    RAW_OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df = download_teams_lookup()

    df.to_csv(
        RAW_OUTPUT_PATH,
        index=False,
        encoding="utf-8"
    )

    print(f"\nOK - Teams lookup saved to {RAW_OUTPUT_PATH}\n")

    print(df.head())


if __name__ == "__main__":
    main()