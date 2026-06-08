def elo_expectancy(
    rating_1: float,
    rating_2: float
) -> float:

    return 1 / (
        1 + 10 ** (
            (rating_2 - rating_1) / 400
        )
    )


def update_elo(
    rating_1: float,
    rating_2: float,
    result: float,
    k_factor: int = 20
):

    expected = elo_expectancy(
        rating_1,
        rating_2
    )

    new_rating = (
        rating_1
        + k_factor
        * (result - expected)
    )

    return round(
        new_rating,
        2
    )


def update_match_elo(
    team_1_rating: float,
    team_2_rating: float,
    team_1_result: float,
    team_2_result: float,
    k_factor: int = 20
):

    return (
        update_elo(
            team_1_rating,
            team_2_rating,
            team_1_result,
            k_factor
        ),
        update_elo(
            team_2_rating,
            team_1_rating,
            team_2_result,
            k_factor
        )
    )
