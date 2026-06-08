from pathlib import Path

import pandas as pd

from src.predictor.calibration import (
    DRAW_BASE_PROBABILITY,
    DRAW_PROBABILITY_CEILING,
    DRAW_PROBABILITY_FLOOR,
)

TEAM_STRENGTH_PATH = Path(
    "data/processed/team_strength.csv"
)

RECENT_FORM_PATH = Path(
    "data/processed/recent_form.csv"
)

HOST_NATIONS = {
    "Mexico",
    "United States",
    "Canada"
}

HOST_ADVANTAGE_ELO = 40

def apply_host_advantage(
    team_name,
    rating
):

    if team_name in HOST_NATIONS:
        return rating + HOST_ADVANTAGE_ELO

    return rating

def elo_expectancy(
    rating_1: float,
    rating_2: float
) -> float:

    return 1 / (
        1 + 10 ** (
            (rating_2 - rating_1) / 400
        )
    )

def get_team_strength(
    strength_df,
    team_name
):

    team_data = strength_df[
        strength_df["team_name"] == team_name
    ]

    if team_data.empty:

        raise ValueError(
            f"Team not found in team_strength: {team_name}"
        )

    return team_data.iloc[0]

def get_form_score(
    form_df,
    country_code
):

    form_data = form_df[
        form_df["country_code"]
        == country_code
    ]

    if form_data.empty:

        raise ValueError(
            f"Form score not found for country code: {country_code}"
        )

    return form_data[
        "form_score"
    ].iloc[0]

def build_stage_features(
    input_matches_path,
    output_features_path,
    stage_name,
    ratings_lookup=None
):
    matches_df = pd.read_csv(
    input_matches_path
   )

    strength_df = pd.read_csv(
        TEAM_STRENGTH_PATH
    )

    form_df = pd.read_csv(
        RECENT_FORM_PATH
    )

    rows = []

    for _, match in matches_df.iterrows():

        team_1 = match["team_a"]
        team_2 = match["team_b"]

        team_1_strength = get_team_strength(
            strength_df,
            team_1
        )

        team_2_strength = get_team_strength(
            strength_df,
            team_2
        )

        team_1_code = team_1_strength[
            "country_code"
        ]

        team_2_code = team_2_strength[
            "country_code"
        ]

        if ratings_lookup:

            rating_1 = ratings_lookup[
                team_1
            ]

            rating_2 = ratings_lookup[
                team_2
            ]

        else:

            rating_1 = team_1_strength[
                "rating"
            ]

            rating_2 = team_2_strength[
                "rating"
            ]

        rating_1 = apply_host_advantage(
            team_1,
            rating_1
        )

        rating_2 = apply_host_advantage(
            team_2,
            rating_2
        )
        
        expectancy = elo_expectancy(
            rating_1,
            rating_2
        )

        team_1_form = get_form_score(
            form_df,
            team_1_code
        )

        team_2_form = get_form_score(
            form_df,
            team_2_code
        )

        form_difference = (
            team_1_form
            - team_2_form
        )

        draw_probability = (
            DRAW_BASE_PROBABILITY
            - abs(expectancy - 0.5)
        )

        draw_probability = max(
            min(draw_probability, DRAW_PROBABILITY_CEILING),
            DRAW_PROBABILITY_FLOOR
        )

        rows.append({
            "match_date": stage_name,
            "team_1_name": team_1,
            "team_2_name": team_2,
            "team_1_rating": rating_1,
            "team_2_rating": rating_2,
            "team_1_win_expectancy": round(expectancy, 3),
            "team_1_form_score": team_1_form,
            "team_2_form_score": team_2_form,
            "form_score_difference": round(
                form_difference,
                3
            ),
            "draw_probability": round(
                draw_probability,
                3
            )
        })

    df = pd.DataFrame(rows)

    df.to_csv(
        output_features_path,
        index=False
    )

    return df


def main():

    df = build_stage_features(
        "data/output/round_of_32_complete.csv",
        "data/processed/round_of_32_features.csv",
        "Round of 32"
    )

    print(df.head())

if __name__ == "__main__":
    main()
