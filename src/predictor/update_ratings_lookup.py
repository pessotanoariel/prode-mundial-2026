from src.predictor.elo_updates import (
    update_elo
)


def update_ratings_lookup(
    ratings_lookup,
    winner,
    loser
):

    winner_rating = ratings_lookup[
        winner
    ]

    loser_rating = ratings_lookup[
        loser
    ]

    ratings_lookup[winner] = (
        update_elo(
            winner_rating,
            loser_rating,
            1.0
        )
    )

    ratings_lookup[loser] = (
        update_elo(
            loser_rating,
            winner_rating,
            0.0
        )
    )

    return ratings_lookup