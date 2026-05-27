from pathlib import Path

import pandas as pd

RAW_RECENT_FORM_PATH = Path("data/processed/recent_form.csv")
RAW_FIXTURES_PATH = Path("data/raw/fixtures.csv")
RAW_TEAMS_PATH = Path("data/raw/teams_lookup.csv")

OUTPUT_PATH = Path("data/processed/upcoming_matches.csv")


def build_upcoming_matches() -> pd.DataFrame:

    fixtures_df = pd.read_csv(RAW_FIXTURES_PATH)

    fixtures_df = fixtures_df[
        fixtures_df["tournament_code"] == "WC"
    ].copy()

    teams_df = pd.read_csv(RAW_TEAMS_PATH)

    recent_form_df = pd.read_csv(RAW_RECENT_FORM_PATH)

    # merge home team names
    df = fixtures_df.merge(
        teams_df[["country_code", "team_name"]],
        left_on="team_1_code",
        right_on="country_code",
        how="left"
    )

    df = df.rename(
        columns={
            "team_name": "team_1_name"
        }
    )

    df = df.merge(
        recent_form_df[
            ["country_code", "form_score"]
        ],
        left_on="team_1_code",
        right_on="country_code",
        how="left"
    )

    df = df.rename(
        columns={
            "form_score": "team_1_form_score"
        }
    )

    df = df.drop(
        columns=["country_code"],
        errors="ignore"
    )

    # merge away team names
    df = df.merge(
        teams_df[["country_code", "team_name"]],
        left_on="team_2_code",
        right_on="country_code",
        how="left"
    )

    df = df.rename(
        columns={
            "team_name": "team_2_name"
        }
    )

    df = df.drop(
        columns=["country_code"],
        errors="ignore"
    )

    df = df.merge(
        recent_form_df[
            ["country_code", "form_score"]
        ],
        left_on="team_2_code",
        right_on="country_code",
        how="left"
    )

    df = df.rename(
        columns={
        "form_score": "team_2_form_score"
        }
    )

    # keep relevant columns
    df = df[
        [
            "match_date",
            "team_1_code",
            "team_1_name",
            "team_2_code",
            "team_2_name",
            "team_1_rating",
            "team_2_rating",
            "team_1_win_expectancy",
            "team_1_form_score",
            "team_2_form_score"
        ]
    ].copy()

    
    df["form_score_difference"] = (
        df["team_1_form_score"]
        - df["team_2_form_score"]
    )

    df["team_1_win_expectancy"] = (
        df["team_1_win_expectancy"] / 100
    )   

    # dynamic draw probability
    df["draw_probability"] = (
        0.30 - (
            abs(df["team_1_win_expectancy"] - 0.5)
        )
    ).clip(lower=0.03, upper=0.25)

    # estimated away win probability
    df["team_2_win_probability"] = (
        1
        - df["team_1_win_expectancy"]
        - df["draw_probability"]
    )

    df["team_2_win_probability"] = (
        df["team_2_win_probability"]
        .clip(lower=0)
            .round(3)
    )

    # clean probabilities
    df["team_1_win_expectancy"] = (
        df["team_1_win_expectancy"]
        .round(3)
    )

    df["draw_probability"] = (
        df["draw_probability"]
        .round(3)
    )

    df["team_1_form_score"] = (
        df["team_1_form_score"]
        .fillna(0)
    )

    df["team_2_form_score"] = (
        df["team_2_form_score"]
        .fillna(0)
    )

    df["form_score_difference"] = (
        df["form_score_difference"]
        .fillna(0)
    )

    return df


def main() -> None:

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df = build_upcoming_matches()

    df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8"
    )

    print(f"\nOK - Upcoming matches dataset saved to {OUTPUT_PATH}\n")

    print(df.head(20))

    print("\nColumns:")
    print(df.columns.tolist())


if __name__ == "__main__":
    main()