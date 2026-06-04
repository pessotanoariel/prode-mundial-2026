from src.predictor.score_model import (
    predict_score
)


def test_home_favorite():

    assert (
        predict_score(
            2.3,
            1.0,
            "France",
            "France",
            "Spain"
        )
        == "2-0"
    )


def test_balanced_match():

    assert (
        predict_score(
            1.4,
            1.4,
            "Draw",
            "France",
            "Spain"
        )
        == "1-1"
    )


def test_away_favorite():

    assert (
        predict_score(
            0.8,
            2.6,
            "Spain",
            "France",
            "Spain"
        )
        == "0-2"
    )


def test_winner_alignment():

    assert (
        predict_score(
            1.4,
            1.4,
            "France",
            "France",
            "Spain"
        )
        == "2-1"
    )