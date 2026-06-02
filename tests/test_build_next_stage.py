import pandas as pd
from pathlib import Path

from src.knockout.build_next_stage import (
    build_next_stage
)


def test_build_next_stage(tmp_path):

    winners_path = (
        tmp_path / "winners.csv"
    )

    output_path = (
        tmp_path / "next_stage.csv"
    )

    winners_df = pd.DataFrame([
        {"winner": "France"},
        {"winner": "Spain"}
    ])

    winners_df.to_csv(
        winners_path,
        index=False
    )

    structure = [
        (101, 89, 90)
    ]

    previous_match_ids = [
        89,
        90
    ]

    result = build_next_stage(
        winners_path,
        structure,
        previous_match_ids,
        output_path
    )

    assert len(result) == 1

    assert (
        result.iloc[0]["team_a"]
        == "France"
    )

    assert (
        result.iloc[0]["team_b"]
        == "Spain"
    )

    assert (
        result.iloc[0]["match_id"]
        == 101
    )