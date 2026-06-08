from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.predictor.elo_updates import (
    elo_expectancy,
    update_match_elo,
)
from src.predictor.generate_predictions import (
    generate_predictions,
)
from src.predictor.ratings_lookup import (
    build_ratings_lookup,
)


INPUT_PATH = Path("data/processed/upcoming_matches.csv")
OUTPUT_PATH = Path("data/output/dynamic_group_predictions_prototype.csv")

PREDICTION_COLUMNS = [
    "match_date",
    "team_1",
    "team_2",
    "team_1_win_probability",
    "draw_probability",
    "team_2_win_probability",
    "predicted_winner",
    "predicted_score",
    "confidence",
    "upset_risk",
]


def calculate_draw_probability(team_1_win_expectancy: float) -> float:
    return round(
        max(
            min(
                0.30 - abs(team_1_win_expectancy - 0.5),
                0.25,
            ),
            0.03,
        ),
        3,
    )


def get_match_results(predicted_score: str) -> tuple[float, float]:
    team_1_goals, team_2_goals = (
        int(score)
        for score in predicted_score.split("-")
    )

    if team_1_goals > team_2_goals:
        return 1.0, 0.0

    if team_1_goals < team_2_goals:
        return 0.0, 1.0

    return 0.5, 0.5


def build_dynamic_match_features(
    match: pd.Series,
    ratings_lookup: dict[str, float],
) -> pd.DataFrame:
    team_1 = match["team_1_name"]
    team_2 = match["team_2_name"]

    team_1_rating = ratings_lookup.get(
        team_1,
        match["team_1_rating"],
    )
    team_2_rating = ratings_lookup.get(
        team_2,
        match["team_2_rating"],
    )
    team_1_win_expectancy = round(
        elo_expectancy(
            team_1_rating,
            team_2_rating,
        ),
        3,
    )

    return pd.DataFrame(
        [
            {
                "match_date": match["match_date"],
                "team_1_name": team_1,
                "team_2_name": team_2,
                "team_1_rating": team_1_rating,
                "team_2_rating": team_2_rating,
                "team_1_win_expectancy": team_1_win_expectancy,
                "team_1_form_score": match["team_1_form_score"],
                "team_2_form_score": match["team_2_form_score"],
                "form_score_difference": match["form_score_difference"],
                "draw_probability": calculate_draw_probability(
                    team_1_win_expectancy
                ),
            }
        ]
    )


def simulate_dynamic_group_predictions(
    matches_df: pd.DataFrame,
    ratings_lookup: dict[str, float] | None = None,
    simulation_mode: bool = False,
) -> pd.DataFrame:
    if ratings_lookup is None:
        ratings_lookup = build_ratings_lookup()

    predictions = []
    ordered_matches = matches_df.sort_values(
        by="match_date",
        kind="stable",
    )

    for _, match in ordered_matches.iterrows():
        features_df = build_dynamic_match_features(
            match,
            ratings_lookup,
        )
        prediction = generate_predictions(
            features_df,
            simulation_mode=simulation_mode,
        ).iloc[0]

        predictions.append(prediction.to_dict())

        team_1 = match["team_1_name"]
        team_2 = match["team_2_name"]
        team_1_result, team_2_result = get_match_results(
            prediction["predicted_score"]
        )
        team_1_rating, team_2_rating = update_match_elo(
            ratings_lookup.get(team_1, match["team_1_rating"]),
            ratings_lookup.get(team_2, match["team_2_rating"]),
            team_1_result,
            team_2_result,
        )

        ratings_lookup[team_1] = team_1_rating
        ratings_lookup[team_2] = team_2_rating

    return pd.DataFrame(
        predictions,
        columns=PREDICTION_COLUMNS,
    )


def main() -> None:
    matches_df = pd.read_csv(INPUT_PATH)
    predictions_df = simulate_dynamic_group_predictions(matches_df)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    predictions_df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8",
    )

    print(f"\nOK - Dynamic group prototype saved to {OUTPUT_PATH}\n")
    print(predictions_df.head(20))


if __name__ == "__main__":
    main()
