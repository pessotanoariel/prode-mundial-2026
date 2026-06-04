from pathlib import Path

import pandas as pd

from src.predictor.generate_predictions import (
    generate_predictions
)



def predict_stage(
    input_features_path,
    output_predictions_path,
    simulation_mode=False
):

    features_df = pd.read_csv(
        input_features_path
    )

    predictions_df = generate_predictions(
        features_df,
        simulation_mode
    )

    predictions_df.to_csv(
        output_predictions_path,
        index=False
    )

    return predictions_df


def main():

    predictions_df = predict_stage(
        "data/processed/round_of_32_features.csv",
        "data/output/round_of_32_predictions.csv"
    )

    print(
        predictions_df.head()
    )


if __name__ == "__main__":
    main()