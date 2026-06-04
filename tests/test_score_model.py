from src.predictor.score_model import (
    predict_score
)


def test_home_favorite():

    assert (
        predict_score(0.80, 0.10)
        == "3-0"
    )


def test_moderate_home_favorite():

    assert (
        predict_score(0.60, 0.20)
        == "2-1"
    )


def test_balanced_match():

    assert (
        predict_score(0.35, 0.35)
        == "1-1"
    )