from pathlib import Path


PROCESSED_DIR = Path("data/processed")
OUTPUT_DIR = Path("data/output")


# Round of 32
ROUND_OF_32_COMPLETE = OUTPUT_DIR / "round_of_32_complete.csv"
ROUND_OF_32_FEATURES = PROCESSED_DIR / "round_of_32_features.csv"
ROUND_OF_32_PREDICTIONS = OUTPUT_DIR / "round_of_32_predictions.csv"
ROUND_OF_32_WINNERS = OUTPUT_DIR / "round_of_32_winners.csv"


# Round of 16
ROUND_OF_16 = OUTPUT_DIR / "round_of_16.csv"
ROUND_OF_16_FEATURES = PROCESSED_DIR / "round_of_16_features.csv"
ROUND_OF_16_PREDICTIONS = OUTPUT_DIR / "round_of_16_predictions.csv"
ROUND_OF_16_WINNERS = OUTPUT_DIR / "round_of_16_winners.csv"


# Quarterfinals
QUARTERFINALS = OUTPUT_DIR / "quarterfinals.csv"
QUARTERFINALS_FEATURES = PROCESSED_DIR / "quarterfinals_features.csv"
QUARTERFINALS_PREDICTIONS = OUTPUT_DIR / "quarterfinals_predictions.csv"
QUARTERFINALS_WINNERS = OUTPUT_DIR / "quarterfinals_winners.csv"


# Semifinals
SEMIFINALS = OUTPUT_DIR / "semifinals.csv"
SEMIFINALS_FEATURES = PROCESSED_DIR / "semifinals_features.csv"
SEMIFINALS_PREDICTIONS = OUTPUT_DIR / "semifinals_predictions.csv"
SEMIFINALS_WINNERS = OUTPUT_DIR / "semifinals_winners.csv"


# Third place
THIRD_PLACE = OUTPUT_DIR / "third_place.csv"
THIRD_PLACE_FEATURES = PROCESSED_DIR / "third_place_features.csv"
THIRD_PLACE_PREDICTIONS = OUTPUT_DIR / "third_place_predictions.csv"
THIRD_PLACE_WINNERS = OUTPUT_DIR / "third_place_winners.csv"


# Final
FINAL = OUTPUT_DIR / "final.csv"
FINAL_FEATURES = PROCESSED_DIR / "final_features.csv"
FINAL_PREDICTIONS = OUTPUT_DIR / "final_predictions.csv"