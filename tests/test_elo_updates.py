from src.predictor.elo_updates import (
    update_elo
)


def test_equal_ratings_win():

    new_rating = update_elo(
        2000,
        2000,
        1.0
    )

    assert new_rating == 2010.0

def test_equal_ratings_draw():

    new_rating = update_elo(
        2000,
        2000,
        0.5
    )

    assert new_rating == 2000.0

def test_equal_ratings_loss():

    new_rating = update_elo(
        2000,
        2000,
        0.0
    )

    assert new_rating == 1990.0