from src.predictor.expected_goals import (
    estimate_expected_goals
)


def test_expected_goals():

    home_xg, away_xg = (
        estimate_expected_goals(
            0.75,
            0.10
        )
    )

    assert home_xg > away_xg