from pathlib import Path

import pandas as pd


RAW_ELO_PATH = Path("data/raw/elo_rankings.csv")
RAW_TEAMS_PATH = Path("data/raw/teams_lookup.csv")

OUTPUT_PATH = Path("data/processed/team_strength.csv")


def build_team_strength() -> pd.DataFrame:

    elo_df = pd.read_csv(RAW_ELO_PATH)

    teams_df = pd.read_csv(RAW_TEAMS_PATH)

    # merge country codes with team names
    df = elo_df.merge(
        teams_df[["country_code", "team_name"]],
        on="country_code",
        how="left"
    )

    # select core columns
    df = df[
        [
            "rank",
            "country_code",
            "team_name",
            "rating",
            "wins",
            "losses",
            "draws",
            "goals_for",
            "goals_against"
        ]
    ].copy()

    # calculate win rate
    total_matches = (
        df["wins"] +
        df["losses"] +
        df["draws"]
    )

    df["win_rate"] = (
        df["wins"] / total_matches
    ).round(3)

    # goal difference
    df["goal_difference"] = (
        df["goals_for"] -
        df["goals_against"]
    )

    # sort by rating
    df = df.sort_values(
        by="rating",
        ascending=False
    )

    return df


def main() -> None:

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df = build_team_strength()

    df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8"
    )

    print(f"\nOK - Team strength dataset saved to {OUTPUT_PATH}\n")

    print(df.head(15))

    print("\nColumns:")
    print(df.columns.tolist())


if __name__ == "__main__":
    main()