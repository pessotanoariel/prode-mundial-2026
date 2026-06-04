import random


def resolve_simulated_winner(
    team_1,
    team_2,
    home_goals,
    away_goals
):

    if home_goals > away_goals:
        return team_1

    if away_goals > home_goals:
        return team_2

    return random.choice(
        [team_1, team_2]
    )