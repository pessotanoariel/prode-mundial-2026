from pathlib import Path

import pandas as pd


ROUND_OF_32_PATH = Path(
    "data/output/round_of_32_complete.csv"
)

TEAM_STRENGTH_PATH = Path(
    "data/processed/team_strength.csv"
)

RECENT_FORM_PATH = Path(
    "data/processed/recent_form.csv"
)

OUTPUT_PATH = Path(
    "data/processed/round_of_32_features.csv"
)


def elo_expectancy(
    rating_1: float,
    rating_2: float
) -> float:

    return 1 / (
        1 + 10 ** (
            (rating_2 - rating_1) / 400
        )
    )


def build_round_of_32_features():

    matches_df = pd.read_csv(
        ROUND_OF_32_PATH
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

        team_1_strength = strength_df[
            strength_df["team_name"] == team_1
        ].iloc[0]

        team_2_strength = strength_df[
            strength_df["team_name"] == team_2
        ].iloc[0]

        team_1_code = team_1_strength[
            "country_code"
        ]

        team_2_code = team_2_strength[
            "country_code"
        ]

        rating_1 = team_1_strength[
            "rating"
        ]

        rating_2 = team_2_strength[
            "rating"
        ]

        expectancy = elo_expectancy(
            rating_1,
            rating_2
        )

        team_1_form = form_df[
            form_df["country_code"]
            == team_1_code
        ]["form_score"].iloc[0]

        team_2_form = form_df[
            form_df["country_code"]
            == team_2_code
        ]["form_score"].iloc[0]

        form_difference = (
            team_1_form
            - team_2_form
        )

        draw_probability = (
            0.30
            - abs(expectancy - 0.5)
        )

        draw_probability = max(
            min(draw_probability, 0.25),
            0.03
        )

        rows.append({
            "match_date": "Round of 32",
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

    return pd.DataFrame(rows)


def main():

    df = build_round_of_32_features()

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(df)


if __name__ == "__main__":
    main()