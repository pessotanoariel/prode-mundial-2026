import pandas as pd

from src.predictor.update_stage_ratings import (
    update_stage_ratings
)


def test_update_stage_ratings(
    tmp_path
):

    winners_path = (
        tmp_path / "winners.csv"
    )

    winners_df = pd.DataFrame([
        {
            "winner": "France",
            "loser": "Spain"
        }
    ])

    winners_df.to_csv(
        winners_path,
        index=False
    )

    ratings_lookup = {
        "France": 2000,
        "Spain": 2000
    }

    update_stage_ratings(
        winners_path,
        ratings_lookup
    )

    assert (
        ratings_lookup["France"]
        == 2010.0
    )

    assert (
        ratings_lookup["Spain"]
        == 1990.0
    )