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

TEAM_STRENGTH_PATH = Path(
    "data/processed/team_strength.csv"
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

def build_head_to_head_table(
    predictions_df: pd.DataFrame,
    teams: list[str]
) -> pd.DataFrame:

    rows = []

    for team in teams:

        rows.append({
            "team": team,
            "H2H_PTS": 0,
            "H2H_DG": 0,
            "H2H_GF": 0
        })

    h2h_df = pd.DataFrame(rows).set_index("team")

    matches = predictions_df[
        predictions_df["team_1"].isin(teams)
        &
        predictions_df["team_2"].isin(teams)
    ]

    for _, match in matches.iterrows():

        team_1 = match["team_1"]
        team_2 = match["team_2"]
        goals_1 = match["team_1_goals"]
        goals_2 = match["team_2_goals"]

        h2h_df.loc[team_1, "H2H_GF"] += goals_1
        h2h_df.loc[team_2, "H2H_GF"] += goals_2
        h2h_df.loc[team_1, "H2H_DG"] += goals_1 - goals_2
        h2h_df.loc[team_2, "H2H_DG"] += goals_2 - goals_1

        if goals_1 > goals_2:
            h2h_df.loc[team_1, "H2H_PTS"] += 3
        elif goals_1 < goals_2:
            h2h_df.loc[team_2, "H2H_PTS"] += 3
        else:
            h2h_df.loc[team_1, "H2H_PTS"] += 1
            h2h_df.loc[team_2, "H2H_PTS"] += 1

    return h2h_df.reset_index()


def load_elo_ratings(
    path: Path = TEAM_STRENGTH_PATH
) -> dict[str, float]:

    if not path.exists():
        return {}

    ratings_df = pd.read_csv(path)

    if "team_name" not in ratings_df.columns or "rating" not in ratings_df.columns:
        return {}

    return dict(
        zip(
            ratings_df["team_name"],
            ratings_df["rating"]
        )
    )


def sort_by_final_fallback(
    group_df: pd.DataFrame,
    elo_ratings: dict[str, float]
) -> list[str]:

    fallback_df = group_df.copy()
    fallback_df["ELO_FALLBACK"] = (
        fallback_df["team"]
        .map(elo_ratings)
        .fillna(0)
    )

    return (
        fallback_df
        .sort_values(
            by=[
                "DG",
                "GF",
                "ELO_FALLBACK",
                "team"
            ],
            ascending=[
                False,
                False,
                False,
                True
            ]
        )
        ["team"]
        .tolist()
    )


def resolve_tied_teams(
    predictions_df: pd.DataFrame,
    group_df: pd.DataFrame,
    teams: list[str],
    elo_ratings: dict[str, float] | None = None
) -> list[str]:

    if elo_ratings is None:
        elo_ratings = {}

    if len(teams) == 1:
        return teams

    h2h_df = build_head_to_head_table(
        predictions_df,
        teams
    )

    h2h_df = h2h_df.sort_values(
        by=[
            "H2H_PTS",
            "H2H_DG",
            "H2H_GF",
            "team"
        ],
        ascending=[
            False,
            False,
            False,
            True
        ]
    )

    criteria = [
        "H2H_PTS",
        "H2H_DG",
        "H2H_GF"
    ]

    grouped = list(
        h2h_df.groupby(
            criteria,
            sort=False
        )
    )

    if len(grouped) == 1:

        fallback_df = group_df[
            group_df["team"].isin(teams)
        ]

        return sort_by_final_fallback(
            fallback_df,
            elo_ratings
        )

    resolved = []

    for _, tied_h2h_df in grouped:

        tied_teams = tied_h2h_df["team"].tolist()

        if len(tied_teams) == 1:
            resolved.extend(tied_teams)
        else:
            resolved.extend(
                resolve_tied_teams(
                    predictions_df,
                    group_df,
                    tied_teams,
                    elo_ratings
                )
            )

    return resolved


def apply_head_to_head_columns(
    standings_df: pd.DataFrame,
    predictions_df: pd.DataFrame
) -> pd.DataFrame:

    standings_df = standings_df.copy()

    for _, group_df in standings_df.groupby("group"):

        for _, tied_df in group_df.groupby("PTS"):

            if len(tied_df) < 2:
                continue

            teams = tied_df["team"].tolist()
            h2h_df = build_head_to_head_table(
                predictions_df,
                teams
            )

            for _, row in h2h_df.iterrows():

                standings_df.loc[
                    standings_df["team"] == row["team"],
                    ["H2H_PTS", "H2H_DG", "H2H_GF"]
                ] = [
                    row["H2H_PTS"],
                    row["H2H_DG"],
                    row["H2H_GF"]
                ]

    return standings_df


def sort_group_standings(
    standings_df: pd.DataFrame,
    predictions_df: pd.DataFrame,
    elo_ratings: dict[str, float] | None = None
) -> pd.DataFrame:

    if elo_ratings is None:
        elo_ratings = load_elo_ratings()

    ordered_groups = []

    for group, group_df in standings_df.groupby(
        "group",
        sort=True
    ):

        group_rows = []

        for _, points_df in (
            group_df
            .sort_values(
                by=[
                    "PTS",
                    "DG",
                    "GF",
                    "team"
                ],
                ascending=[
                    False,
                    False,
                    False,
                    True
                ]
            )
            .groupby(
                "PTS",
                sort=False
            )
        ):

            if len(points_df) == 1:
                group_rows.append(points_df.iloc[0])
                continue

            ordered_teams = resolve_tied_teams(
                predictions_df,
                group_df,
                points_df["team"].tolist(),
                elo_ratings
            )

            for team in ordered_teams:
                group_rows.append(
                    points_df[
                        points_df["team"] == team
                    ].iloc[0]
                )

        ordered_group_df = pd.DataFrame(group_rows)
        ordered_group_df["group"] = group
        ordered_groups.append(ordered_group_df)

    return pd.concat(
        ordered_groups,
        ignore_index=True
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
    
    standings_df = apply_head_to_head_columns(
        standings_df,
        predictions_df
    )

    standings_df = sort_group_standings(
        standings_df,
        predictions_df,
        load_elo_ratings()
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
