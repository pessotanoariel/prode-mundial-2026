from src.predictor.poisson_model import (
    most_likely_goals
)

from src.predictor.poisson_model import (
    sample_goals
)


def predict_score(
    home_xg,
    away_xg,
    predicted_winner,
    team_1,
    team_2
):

    home_goals = most_likely_goals(
        home_xg
    )

    away_goals = most_likely_goals(
        away_xg
    )

    if predicted_winner == "Draw":

        return (
            f"{home_goals}-{away_goals}"
        )

    if (
        predicted_winner == team_1
        and home_goals <= away_goals
    ):

        home_goals = away_goals + 1

    if (
        predicted_winner == team_2
        and away_goals <= home_goals
    ):

        away_goals = home_goals + 1

    return (
        f"{home_goals}-{away_goals}"
    )

def simulate_score(
    home_xg,
    away_xg
):

    home_goals = sample_goals(
        home_xg
    )

    away_goals = sample_goals(
        away_xg
    )

    return (
        home_goals,
        away_goals
    )