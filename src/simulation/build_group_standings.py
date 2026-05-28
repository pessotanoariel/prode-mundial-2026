from pathlib import Path

import pandas as pd

PREDICTIONS_PATH = Path(
    "data/output/predictions.csv"
)

GROUPS_PATH = Path(
    "data/raw/world_cup_groups.csv"
)

OUTPUT_PATH = Path(
    "data/output/group_standings.csv"
)

def build_group_standings() -> pd.DataFrame:

    predictions_df = pd.read_csv(PREDICTIONS_PATH)

    groups_df = pd.read_csv(GROUPS_PATH)

    team_group_mapping = (
        groups_df[
            ["country", "group"]
        ]
        .rename(
            columns={
                "country": "team"
            }
        )
    )

    scores = predictions_df[
        "predicted_score"
    ].str.split(
        "-",
        expand=True
    )

    predictions_df["team_1_goals"] = (
        scores[0]
        .astype(int)
    )

    predictions_df["team_2_goals"] = (
        scores[1]
        .astype(int)
    )

    teams = pd.concat(
        [
            predictions_df["team_1"],
            predictions_df["team_2"]
        ]
    ).unique()

    standings_df = pd.DataFrame({
        "team": teams,
        "PJ": 0,
        "PG": 0,
        "PE": 0,
        "PP": 0,
        "GF": 0,
        "GC": 0,
        "DG": 0,
        "PTS": 0
    })

    for _, row in predictions_df.iterrows():

        team_1 = row["team_1"]
        team_2 = row["team_2"]

        goals_1 = row["team_1_goals"]
        goals_2 = row["team_2_goals"]

        # matches played
        standings_df.loc[
            standings_df["team"] == team_1,
            "PJ"
        ] += 1

        standings_df.loc[
            standings_df["team"] == team_2,
            "PJ"
        ] += 1

        # goals for
        standings_df.loc[
            standings_df["team"] == team_1,
            "GF"
        ] += goals_1

        standings_df.loc[
            standings_df["team"] == team_2,
            "GF"
        ] += goals_2

        # goals against
        standings_df.loc[
            standings_df["team"] == team_1,
            "GC"
        ] += goals_2

        standings_df.loc[
            standings_df["team"] == team_2,
            "GC"
        ] += goals_1

        # wins / draws / losses
        if goals_1 > goals_2:

            standings_df.loc[
                standings_df["team"] == team_1,
                "PG"
            ] += 1

            standings_df.loc[
                standings_df["team"] == team_2,
                "PP"
            ] += 1

            standings_df.loc[
                standings_df["team"] == team_1,
                "PTS"
            ] += 3

        elif goals_1 < goals_2:

            standings_df.loc[
                standings_df["team"] == team_2,
                "PG"
            ] += 1

            standings_df.loc[
                standings_df["team"] == team_1,
                "PP"
            ] += 1

            standings_df.loc[
                standings_df["team"] == team_2,
                "PTS"
            ] += 3

        else:

            standings_df.loc[
                standings_df["team"] == team_1,
                "PE"
            ] += 1

            standings_df.loc[
                standings_df["team"] == team_2,
                "PE"
            ] += 1

            standings_df.loc[
                standings_df["team"] == team_1,
                "PTS"
            ] += 1

            standings_df.loc[
                standings_df["team"] == team_2,
                "PTS"
            ] += 1

    standings_df["DG"] = (
        standings_df["GF"]
        - standings_df["GC"]
    )

    standings_df = standings_df.sort_values(
        by=[
            "PTS",
            "DG",
            "GF"
        ],
        ascending=False
    )

    standings_df = standings_df.merge(
        team_group_mapping,
        on="team",
        how="left"
    )
    
    return standings_df

def main() -> None:

    df = build_group_standings()

    print(df.head())


if __name__ == "__main__":
    main()