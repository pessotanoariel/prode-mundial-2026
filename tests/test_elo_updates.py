from src.predictor.elo_updates import (
    update_match_elo,
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


def test_match_win_loss_updates_ratings_in_opposite_directions():

    team_1_rating, team_2_rating = update_match_elo(
        2000,
        2000,
        1.0,
        0.0
    )

    assert team_1_rating == 2010.0
    assert team_2_rating == 1990.0


def test_match_draw_updates_both_teams_correctly():

    team_1_rating, team_2_rating = update_match_elo(
        2100,
        1900,
        0.5,
        0.5
    )

    assert team_1_rating == 2094.81
    assert team_2_rating == 1905.19
