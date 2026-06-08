from src.predictor.elo_updates import (
    update_match_elo
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

    winner_new_rating, loser_new_rating = update_match_elo(
        winner_rating,
        loser_rating,
        1.0,
        0.0
    )

    ratings_lookup[winner] = winner_new_rating
    ratings_lookup[loser] = loser_new_rating

    return ratings_lookup
