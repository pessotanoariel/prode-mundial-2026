from src.predictor.poisson_model import (
    sample_goals
)


def test_sample_goals():

    result = sample_goals(
        2.0
    )

    assert isinstance(
        result,
        int
    )

    assert result >= 0