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


def test_update_ratings_lookup_preserves_knockout_winner_loser_behavior():

    ratings_lookup = {
        "Argentina": 2050,
        "Brazil": 1950
    }

    returned_lookup = update_ratings_lookup(
        ratings_lookup,
        "Argentina",
        "Brazil"
    )

    assert returned_lookup is ratings_lookup
    assert ratings_lookup["Argentina"] == 2057.2
    assert ratings_lookup["Brazil"] == 1942.8
