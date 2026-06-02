from src.knockout.build_next_stage import (
    build_next_stage
)

from src.knockout.structures import (
    SEMIFINAL_STRUCTURE
)


def build_semifinals():

    return build_next_stage(
        "data/output/quarterfinals_winners.csv",
        SEMIFINAL_STRUCTURE,
        "data/output/semifinals.csv"
    )


if __name__ == "__main__":

    print(
        build_semifinals()
    )