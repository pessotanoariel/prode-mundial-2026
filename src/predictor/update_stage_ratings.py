import pandas as pd

from src.predictor.update_ratings_lookup import (
    update_ratings_lookup
)


def update_stage_ratings(
    winners_path,
    ratings_lookup
):

    winners_df = pd.read_csv(
        winners_path
    )

    for _, row in winners_df.iterrows():

        update_ratings_lookup(
            ratings_lookup,
            row["winner"],
            row["loser"]
        )

    return ratings_lookup