def estimate_expected_goals(
    home_prob,
    away_prob
):

    home_xg = (
        0.8 + (home_prob * 2.0)
    )

    away_xg = (
        0.8 + (away_prob * 2.0)
    )

    return (
        round(home_xg, 2),
        round(away_xg, 2)
    )