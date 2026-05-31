from pathlib import Path
import pandas as pd
from src.knockout.structures import (
    ROUND_OF_16_STRUCTURE
)


INPUT_PATH = Path(
    "data/output/round_of_32_predictions.csv"
)

OUTPUT_PATH = Path(
    "data/output/round_of_16.csv"
)

def build_round_of_16():

    predictions_df = pd.read_csv(
        INPUT_PATH
    )

    winner_lookup = {}

    for idx, row in predictions_df.iterrows():

        match_id = 73 + idx

        winner_lookup[match_id] = (
            row["predicted_winner"]
        )

    rows = []

    for (
        match_id,
        previous_match_1,
        previous_match_2
    ) in ROUND_OF_16_STRUCTURE:

        rows.append({
            "match_id": match_id,
            "team_a": winner_lookup[
                previous_match_1
            ],
            "team_b": winner_lookup[
                previous_match_2
            ]
        })

    df = pd.DataFrame(rows)

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(df)


if __name__ == "__main__":
    build_round_of_16()