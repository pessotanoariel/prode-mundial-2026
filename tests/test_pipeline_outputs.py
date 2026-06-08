from pathlib import Path

import pandas as pd
import pytest


CRITICAL_OUTPUTS = (
    (
        Path("data/output/champion_probabilities.csv"),
        {"team", "probability"},
    ),
    (
        Path("data/output/most_likely_finals.csv"),
        {"team_1", "team_2"},
    ),
    (
        Path("data/output/team_progression_probabilities.csv"),
        {"team", "qf", "sf", "final", "champion"},
    ),
    (
        Path("data/output/group_standings.csv"),
        {"team", "group", "position", "PTS"},
    ),
    (
        Path("data/output/qualified_teams.csv"),
        {"team"},
    ),
    (
        Path("data/output/final_predictions.csv"),
        {"team_1", "team_2", "predicted_winner", "predicted_score"},
    ),
)


@pytest.mark.parametrize(("path", "expected_columns"), CRITICAL_OUTPUTS)
def test_critical_pipeline_output_exists_and_has_expected_columns(
    path,
    expected_columns,
):
    assert path.exists(), f"Missing pipeline output: {path}"
    assert path.stat().st_size > 0, f"Pipeline output is empty: {path}"

    df = pd.read_csv(path)

    assert not df.empty, f"Pipeline output has no rows: {path}"
    assert expected_columns.issubset(df.columns), (
        f"Missing expected columns in {path}: "
        f"{sorted(expected_columns - set(df.columns))}"
    )
