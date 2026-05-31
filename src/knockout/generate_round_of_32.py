import pandas as pd

from src.knockout.structures import (
    ROUND_OF_32_STRUCTURE
)


def generate_round_of_32_structure(output_path="data/processed/round_of_32_structure.csv"):
    df = pd.DataFrame(ROUND_OF_32_STRUCTURE)
    df["stage"] = "Round of 32"
    df.to_csv(output_path, index=False)
    print(f"✅ Round of 32 structure exported to {output_path}")


if __name__ == "__main__":
    generate_round_of_32_structure()