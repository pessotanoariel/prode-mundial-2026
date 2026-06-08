import pandas as pd

from src.simulation.dynamic_group_simulator import (
    PREDICTION_COLUMNS,
    get_match_results,
    simulate_dynamic_group_predictions,
)


def test_get_match_results_supports_win_loss_and_draw():

    assert get_match_results("2-1") == (1.0, 0.0)
    assert get_match_results("1-2") == (0.0, 1.0)
    assert get_match_results("1-1") == (0.5, 0.5)


def test_dynamic_group_simulator_preserves_prediction_schema_and_updates_elo():

    matches_df = pd.DataFrame(
        [
            {
                "match_date": "2026-06-01",
                "team_1_name": "Alpha",
                "team_2_name": "Beta",
                "team_1_rating": 2000,
                "team_2_rating": 2000,
                "team_1_form_score": 20,
                "team_2_form_score": 0,
                "form_score_difference": 20,
            },
            {
                "match_date": "2026-06-02",
                "team_1_name": "Alpha",
                "team_2_name": "Beta",
                "team_1_rating": 2000,
                "team_2_rating": 2000,
                "team_1_form_score": 20,
                "team_2_form_score": 0,
                "form_score_difference": 20,
            },
        ]
    )
    ratings_lookup = {
        "Alpha": 2000,
        "Beta": 2000,
    }

    predictions_df = simulate_dynamic_group_predictions(
        matches_df,
        ratings_lookup,
    )

    assert predictions_df.columns.tolist() == PREDICTION_COLUMNS
    assert len(predictions_df) == 2
    assert ratings_lookup["Alpha"] > 2000
    assert ratings_lookup["Beta"] < 2000
    assert (
        predictions_df.iloc[1]["team_1_win_probability"]
        > predictions_df.iloc[0]["team_1_win_probability"]
    )
