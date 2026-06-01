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

from src.knockout.paths import (
    ROUND_OF_32_COMPLETE,
    ROUND_OF_32_FEATURES,
    ROUND_OF_32_PREDICTIONS,
    ROUND_OF_32_WINNERS,
    ROUND_OF_16,
    ROUND_OF_16_FEATURES,
    ROUND_OF_16_PREDICTIONS,
    ROUND_OF_16_WINNERS,
    QUARTERFINALS,
    QUARTERFINALS_FEATURES,
    QUARTERFINALS_PREDICTIONS,
    QUARTERFINALS_WINNERS,
    SEMIFINALS,
    SEMIFINALS_FEATURES,
    SEMIFINALS_PREDICTIONS,
    SEMIFINALS_WINNERS,
    THIRD_PLACE,
    THIRD_PLACE_FEATURES,
    THIRD_PLACE_PREDICTIONS,
    THIRD_PLACE_WINNERS,
    FINAL,
    FINAL_FEATURES,
    FINAL_PREDICTIONS
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
        ROUND_OF_32_COMPLETE,
        ROUND_OF_32_FEATURES,
        ROUND_OF_32_PREDICTIONS,
        ROUND_OF_32_WINNERS
    )

    print("\n=== ROUND OF 16 ===")

    build_round_of_16()

    run_stage(
        "Round of 16",
        ROUND_OF_16,
        ROUND_OF_16_FEATURES,
        ROUND_OF_16_PREDICTIONS,
        ROUND_OF_16_WINNERS
    )

    print("\n=== QUARTERFINALS ===")

    build_quarterfinals()

    run_stage(
        "Quarterfinals",
        QUARTERFINALS,
        QUARTERFINALS_FEATURES,
        QUARTERFINALS_PREDICTIONS,
        QUARTERFINALS_WINNERS
    )

    print("\n=== SEMIFINALS ===")

    build_semifinals()

    run_stage(
        "Semifinals",
        SEMIFINALS,
        SEMIFINALS_FEATURES,
        SEMIFINALS_PREDICTIONS,
        SEMIFINALS_WINNERS
    )

    print("\n=== THIRD PLACE ===")

    build_third_place()

    run_stage(
        "Third Place",
        THIRD_PLACE,
        THIRD_PLACE_FEATURES,
        THIRD_PLACE_PREDICTIONS,
        THIRD_PLACE_WINNERS
    )

    print("\n=== FINAL ===")

    build_final()

    run_stage(
        "Final",
        FINAL,
        FINAL_FEATURES,
        FINAL_PREDICTIONS,
        None
    )

    print("\nTournament simulation completed")

if __name__ == "__main__":
    main()