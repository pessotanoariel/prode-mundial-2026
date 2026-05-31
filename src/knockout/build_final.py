from src.knockout.build_next_stage import (
    build_next_stage
)

from src.knockout.structures import (
    FINAL_STRUCTURE
)


def build_final():

    return build_next_stage(
        "data/output/semifinals_winners.csv",
        FINAL_STRUCTURE,
        [101, 102],
        "data/output/final.csv"
    )


if __name__ == "__main__":

    print(
        build_final()
    )