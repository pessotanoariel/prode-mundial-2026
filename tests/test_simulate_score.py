from src.predictor.score_model import (
    simulate_score
)

def test_simulate_score():

    home, away = simulate_score(
        2.3,
        1.0
    )

    assert isinstance(home, int)
    assert isinstance(away, int)

    assert home >= 0
    assert away >= 0