from pathlib import Path

import pandas as pd


TEAM_STRENGTH_PATH = Path(
    "data/processed/team_strength.csv"
)


def build_ratings_lookup(
    team_strength_path=TEAM_STRENGTH_PATH
):

    strength_df = pd.read_csv(
        team_strength_path
    )

    return dict(
        zip(
            strength_df["team_name"],
            strength_df["rating"]
        )
    )