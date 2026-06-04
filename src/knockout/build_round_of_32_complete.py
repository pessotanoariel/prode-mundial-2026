import pandas as pd

from src.knockout.slot_mapping import build_slot_mapping
from src.knockout.best_third_teams import get_best_third_teams
from src.knockout.annex_c import get_annex_c_matchups

import logging

logger = logging.getLogger(__name__)


def build_round_of_32_complete():

    slot_mapping = build_slot_mapping()

    best_thirds = get_best_third_teams()

    best_third_groups = (
        best_thirds["group"]
        .tolist()
    )

    annex_mapping = get_annex_c_matchups(
        best_third_groups
    )

    df = pd.read_csv(
        "data/processed/round_of_32_real_teams.csv"
    )

    third_place_slots = [
        "1A",
        "1B",
        "1D",
        "1E",
        "1G",
        "1I",
        "1K",
        "1L",
    ]

    for winner_slot, third_slot in annex_mapping.items():

        third_team = slot_mapping[third_slot]

        mask = (
            df["team_a_slot"] == winner_slot
        )

        df.loc[
            mask,
            "team_b"
        ] = third_team

    output_path = (
        "data/output/round_of_32_complete.csv"
    )

    df.to_csv(
        output_path,
        index=False
    )

    logger.info(
        f"Exported {output_path}"
    )


if __name__ == "__main__":
    build_round_of_32_complete()