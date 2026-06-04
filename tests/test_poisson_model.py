from src.predictor.poisson_model import (
    most_likely_goals
)


def test_most_likely_goals():

    goals = most_likely_goals(
        2.1
    )

    assert goals == 2