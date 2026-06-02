import pandas as pd

from src.knockout.resolve_knockout_winners import (
    resolve_knockout_winners
)


def test_regular_time_winner():

    predictions_df = pd.DataFrame([
        {
            "team_1": "France",
            "team_2": "Spain",
            "predicted_winner": "France",
            "team_1_win_probability": 0.60,
            "team_2_win_probability": 0.30
        }
    ])

    result = resolve_knockout_winners(
        predictions_df
    )

    assert result.iloc[0]["winner"] == "France"
    assert result.iloc[0]["loser"] == "Spain"
    assert (
        result.iloc[0]["resolution"]
        == "Regular Time"
    )

def test_extra_time_resolution():

    predictions_df = pd.DataFrame([
        {
            "team_1": "France",
            "team_2": "Spain",
            "predicted_winner": "Draw",
            "team_1_win_probability": 0.55,
            "team_2_win_probability": 0.45
        }
    ])

    result = resolve_knockout_winners(
        predictions_df
    )

    assert result.iloc[0]["winner"] == "France"
    assert (
        result.iloc[0]["resolution"]
        == "Extra Time"
    )

def test_penalties_resolution():

    predictions_df = pd.DataFrame([
        {
            "team_1": "France",
            "team_2": "Spain",
            "predicted_winner": "Draw",
            "team_1_win_probability": 0.52,
            "team_2_win_probability": 0.48
        }
    ])

    result = resolve_knockout_winners(
        predictions_df
    )

    assert result.iloc[0]["winner"] == "France"
    assert (
        result.iloc[0]["resolution"]
        == "Penalties"
    )