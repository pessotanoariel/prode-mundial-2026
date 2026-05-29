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

QUALIFIED_PATH = Path(
    "data/output/qualified_teams.csv"
)

def get_head_to_head_stats(
    predictions_df: pd.DataFrame,
    team_a: str,
    team_b: str
) -> dict:

    h2h_match = predictions_df[
        (
            (predictions_df["team_1"] == team_a)
            &
            (predictions_df["team_2"] == team_b)
        )
        |
        (
            (predictions_df["team_1"] == team_b)
            &
            (predictions_df["team_2"] == team_a)
        )
    ]

    if h2h_match.empty:

        return {
            "PTS": 0,
            "DG": 0,
            "GF": 0
        }

    match = h2h_match.iloc[0]

    if match["team_1"] == team_a:

        goals_for = match["team_1_goals"]
        goals_against = match["team_2_goals"]

    else:

        goals_for = match["team_2_goals"]
        goals_against = match["team_1_goals"]

    if goals_for > goals_against:

        points = 3

    elif goals_for < goals_against:

        points = 0

    else:

        points = 1

    return {
        "PTS": points,
        "DG": goals_for - goals_against,
        "GF": goals_for
    }

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
        "PTS": 0,
        "H2H_PTS": 0,
        "H2H_DG": 0,
        "H2H_GF": 0
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

    standings_df = standings_df.merge(
        team_group_mapping,
        on="team",
        how="left"
    )
    
    for group, group_df in standings_df.groupby("group"):

        duplicated_points = group_df[
            group_df["PTS"].duplicated(keep=False)
        ]

        if len(duplicated_points) == 2:

            team_a = duplicated_points.iloc[0]["team"]
            team_b = duplicated_points.iloc[1]["team"]

            team_a_stats = get_head_to_head_stats(
                predictions_df,
                team_a,
                team_b
            )

            team_b_stats = get_head_to_head_stats(
                predictions_df,
             team_b,
                team_a
            )

            standings_df.loc[
                standings_df["team"] == team_a,
                ["H2H_PTS", "H2H_DG", "H2H_GF"]
            ] = [
                team_a_stats["PTS"],
                team_a_stats["DG"],
                team_a_stats["GF"]
            ]

            standings_df.loc[
                standings_df["team"] == team_b,
                ["H2H_PTS", "H2H_DG", "H2H_GF"]
            ] = [
                team_b_stats["PTS"],
                team_b_stats["DG"],
                team_b_stats["GF"]
            ]
    
    standings_df = standings_df.sort_values(
        by=[
            "group",
            "PTS",
            "H2H_PTS",
            "H2H_DG",
            "H2H_GF",
            "DG",
            "GF"
        ],
        ascending=[
            True,
            False,
            False,
            False,
            False,
            False,
            False
        ]   
    )

    standings_df["position"] = (
        standings_df.groupby("group")
        .cumcount()
        + 1
    )

    third_place_df = standings_df[
        standings_df["position"] == 3
    ].copy()

    third_place_df = third_place_df.sort_values(
        by=[
            "PTS",
            "DG",
            "GF"
        ],
        ascending=[
            False,
            False,
            False
        ]
    )

    best_thirds = third_place_df.head(8).copy()

    qualified_teams = standings_df[
        standings_df["position"] <= 2
    ].copy()

    qualified_teams = pd.concat(
        [
            qualified_teams,
            best_thirds
        ]
    )

    qualified_teams = qualified_teams.sort_values(
    by=[
        "group",
        "position"
    ]
    )

    standings_df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    qualified_teams.to_csv(
        QUALIFIED_PATH,
        index=False
    )

    return standings_df

def main() -> None:

    df = build_group_standings()

    print(df.head())


if __name__ == "__main__":
    main()