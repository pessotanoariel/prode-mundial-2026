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