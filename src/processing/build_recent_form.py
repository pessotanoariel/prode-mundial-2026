from pathlib import Path

import pandas as pd


RAW_RESULTS_PATH = Path("data/raw/latest_results.csv")

OUTPUT_PATH = Path("data/processed/recent_form.csv")


def calculate_match_points(goals_for, goals_against):

    if goals_for > goals_against:
        return 3

    if goals_for == goals_against:
        return 1

    return 0


def build_recent_form() -> pd.DataFrame:

    df = pd.read_csv(RAW_RESULTS_PATH)

    home_df = df[
        [
            "match_date",
            "team_1_code",
            "team_1_goals",
            "team_2_goals"
        ]
    ].copy()

    home_df.columns = [
        "match_date",
        "country_code",
        "goals_for",
        "goals_against"
    ]

    away_df = df[
        [
            "match_date",
            "team_2_code",
            "team_2_goals",
            "team_1_goals"
        ]
    ].copy()

    away_df.columns = [
        "match_date",
        "country_code",
        "goals_for",
        "goals_against"
    ]

    matches_df = pd.concat(
        [home_df, away_df],
        ignore_index=True
    )

    matches_df["match_date"] = pd.to_datetime(
        matches_df["match_date"]
    )

    matches_df = matches_df.sort_values(
        by="match_date",
        ascending=False
    )

    matches_df["points"] = matches_df.apply(
        lambda row: calculate_match_points(
            row["goals_for"],
            row["goals_against"]
        ),
        axis=1
    )

    matches_df["goal_difference"] = (
        matches_df["goals_for"]
        - matches_df["goals_against"]
    )

    recent_form_df = (
        matches_df
        .groupby("country_code")
        .head(5)
        .groupby("country_code")
        .agg({
            "points": "sum",
            "goal_difference": "sum",
            "goals_for": "sum",
            "goals_against": "sum"
        })
        .reset_index()
    )

    recent_form_df["form_score"] = (
        recent_form_df["points"] * 0.7
        + recent_form_df["goal_difference"] * 0.3
    ).round(2)

    return recent_form_df


def main() -> None:

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df = build_recent_form()

    df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8"
    )

    print(f"\nOK - Recent form dataset saved to {OUTPUT_PATH}\n")

    print(df.head(20))


if __name__ == "__main__":
    main()