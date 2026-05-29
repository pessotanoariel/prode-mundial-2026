from pathlib import Path

import pandas as pd

from src.predictor.generate_predictions import (
    generate_predictions
)

INPUT_PATH = Path(
    "data/processed/round_of_32_features.csv"
)

OUTPUT_PATH = Path(
    "data/output/round_of_32_predictions.csv"
)


def main():

    matches_df = pd.read_csv(
        INPUT_PATH
    )

    predictions_df = generate_predictions(
        matches_df
    )

    predictions_df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(predictions_df)


if __name__ == "__main__":
    main()