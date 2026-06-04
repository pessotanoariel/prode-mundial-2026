from src.predictor.poisson_model import (
    most_likely_goals
)


def predict_score(
    home_xg,
    away_xg
):

    home_goals = most_likely_goals(
        home_xg
    )

    away_goals = most_likely_goals(
        away_xg
    )

    return (
        f"{home_goals}-{away_goals}"
    )