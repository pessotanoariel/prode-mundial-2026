from src.knockout.build_round_of_32_complete import (
    build_round_of_32_complete
)

from src.knockout.stage_features import (
    build_stage_features
)

from src.knockout.stage_predictions import (
    predict_stage
)

from src.knockout.resolve_knockout_winners import (
    save_winners
)

from src.knockout.build_round_of_16 import (
    build_round_of_16
)

from src.knockout.build_quarterfinals import (
    build_quarterfinals
)

from src.knockout.build_semifinals import (
    build_semifinals
)

from src.knockout.build_third_place import (
    build_third_place
)

from src.knockout.build_final import (
    build_final
)

def run_stage(
    stage_name,
    matches_path,
    features_path,
    predictions_path,
    winners_path=None
):
    print(f"Building features: {stage_name}")
    build_stage_features(
        matches_path,
        features_path,
        stage_name
    )

    print(f"Generating predictions: {stage_name}")
    predict_stage(
        features_path,
        predictions_path
    )

    if winners_path:

        print(f"Resolving winners: {stage_name}")

        save_winners(
            predictions_path,
            winners_path
        )

def main():

    print("\n=== ROUND OF 32 ===")

    build_round_of_32_complete()

    run_stage(
        "Round of 32",
        "data/output/round_of_32_complete.csv",
        "data/processed/round_of_32_features.csv",
        "data/output/round_of_32_predictions.csv",
        "data/output/round_of_32_winners.csv"
    )

    print("\n=== ROUND OF 16 ===")

    build_round_of_16()

    run_stage(
        "Round of 16",
        "data/output/round_of_16.csv",
        "data/processed/round_of_16_features.csv",
        "data/output/round_of_16_predictions.csv",
        "data/output/round_of_16_winners.csv"
    )

    print("\n=== QUARTERFINALS ===")

    build_quarterfinals()

    run_stage(
        "Quarterfinals",
        "data/output/quarterfinals.csv",
        "data/processed/quarterfinals_features.csv",
        "data/output/quarterfinals_predictions.csv",
        "data/output/quarterfinals_winners.csv"
    )

    print("\n=== SEMIFINALS ===")

    build_semifinals()

    run_stage(
        "Semifinals",
        "data/output/semifinals.csv",
        "data/processed/semifinals_features.csv",
        "data/output/semifinals_predictions.csv",
        "data/output/semifinals_winners.csv"
    )

    print("\n=== THIRD PLACE ===")

    build_third_place()

    run_stage(
        "Third Place",
        "data/output/third_place.csv",
        "data/processed/third_place_features.csv",
        "data/output/third_place_predictions.csv",
        "data/output/third_place_winners.csv"
    )

    print("\n=== FINAL ===")

    build_final()

    run_stage(
        "Final",
        "data/output/final.csv",
        "data/processed/final_features.csv",
        "data/output/final_predictions.csv",
        None
    )

    print("\nTournament simulation completed")

if __name__ == "__main__":
    main()