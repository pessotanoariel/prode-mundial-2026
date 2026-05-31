from src.knockout.build_next_stage import (
    build_next_stage
)

from src.knockout.structures import (
    QUARTERFINAL_STRUCTURE
)


def build_quarterfinals():

    return build_next_stage(
        "data/output/round_of_16_winners.csv",
        QUARTERFINAL_STRUCTURE,
        [89, 90, 91, 92, 93, 94, 95, 96],
        "data/output/quarterfinals.csv"
    )


if __name__ == "__main__":

    print(
        build_quarterfinals()
    )