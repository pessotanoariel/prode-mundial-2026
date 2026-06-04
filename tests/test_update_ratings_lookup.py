from src.predictor.update_ratings_lookup import (
    update_ratings_lookup
)


def test_update_ratings_lookup():

    ratings_lookup = {
        "France": 2000,
        "Spain": 2000
    }

    update_ratings_lookup(
        ratings_lookup,
        "France",
        "Spain"
    )

    assert (
        ratings_lookup["France"]
        == 2010.0
    )

    assert (
        ratings_lookup["Spain"]
        == 1990.0
    )