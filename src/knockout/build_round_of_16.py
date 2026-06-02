from src.knockout.build_next_stage import (
    build_next_stage
)

from src.knockout.structures import (
    ROUND_OF_16_STRUCTURE
)


def build_round_of_16():

    return build_next_stage(
        "data/output/round_of_32_winners.csv",
        ROUND_OF_16_STRUCTURE,
        "data/output/round_of_16.csv"
    )


if __name__ == "__main__":

    print(
        build_round_of_16()
    )