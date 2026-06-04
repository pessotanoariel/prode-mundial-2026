import pandas as pd

from src.predictor.ratings_lookup import (
    build_ratings_lookup
)


def test_build_ratings_lookup(
    tmp_path
):

    team_strength_path = (
        tmp_path / "team_strength.csv"
    )

    team_strength_df = pd.DataFrame([
        {
            "team_name": "France",
            "rating": 2050
        },
        {
            "team_name": "Spain",
            "rating": 2025
        }
    ])

    team_strength_df.to_csv(
        team_strength_path,
        index=False
    )

    ratings_lookup = (
        build_ratings_lookup(
            team_strength_path
        )
    )

    assert (
        ratings_lookup["France"]
        == 2050
    )

    assert (
        ratings_lookup["Spain"]
        == 2025
    )

    assert len(
        ratings_lookup
    ) == 2