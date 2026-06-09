import pandas as pd

from src.simulation import monte_carlo


def write_winners(path, winners):
    pd.DataFrame(
        [
            {
                "winner": winner,
            }
            for winner in winners
        ]
    ).to_csv(
        path,
        index=False,
    )


def test_run_monte_carlo_tracks_both_finalists(tmp_path, monkeypatch):
    output_dir = tmp_path / "data" / "output"
    output_dir.mkdir(
        parents=True,
    )

    quarterfinals_path = output_dir / "quarterfinals_winners.csv"
    semifinals_path = output_dir / "semifinals_winners.csv"
    final_winners_path = output_dir / "final_winners.csv"
    predictions_path = output_dir / "predictions.csv"

    write_winners(
        quarterfinals_path,
        [
            "Alpha",
            "Beta",
        ],
    )
    write_winners(
        semifinals_path,
        [
            "Alpha",
            "Beta",
        ],
    )
    pd.DataFrame(
        [
            {
                "match_date": "Final",
                "team_1": "Alpha",
                "team_2": "Beta",
                "team_1_win_probability": 0.6,
                "draw_probability": 0.1,
                "team_2_win_probability": 0.3,
                "predicted_winner": "Alpha",
                "predicted_score": "2-1",
                "confidence": "High",
                "upset_risk": "LOW",
            }
        ]
    ).to_csv(
        predictions_path,
        index=False,
    )

    def fake_simulation_main():
        pd.DataFrame(
            [
                {
                    "team_1": "Alpha",
                    "team_2": "Beta",
                    "winner": "Alpha",
                    "loser": "Beta",
                    "resolution": "Regular Time",
                }
            ]
        ).to_csv(
            final_winners_path,
            index=False,
        )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        monte_carlo,
        "simulation_main",
        fake_simulation_main,
    )
    monkeypatch.setattr(
        monte_carlo,
        "FINAL_WINNERS_PATH",
        str(final_winners_path),
    )
    monkeypatch.setattr(
        monte_carlo,
        "QUARTERFINALS_WINNERS",
        quarterfinals_path,
    )
    monkeypatch.setattr(
        monte_carlo,
        "SEMIFINALS_WINNERS",
        semifinals_path,
    )
    monkeypatch.setattr(
        monte_carlo,
        "KNOCKOUT_STAGES",
        [
            {
                "stage": "Final",
                "matches_path": tmp_path / "data" / "output" / "final.csv",
                "winners_path": final_winners_path,
            }
        ],
    )
    pd.DataFrame(
        [
            {
                "match_id": 103,
                "team_a": "Alpha",
                "team_b": "Beta",
            }
        ]
    ).to_csv(
        tmp_path / "data" / "output" / "final.csv",
        index=False,
    )

    monte_carlo.run_monte_carlo(
        simulations=1,
    )

    finalist_df = pd.read_csv(
        output_dir / "finalist_probabilities.csv"
    )
    progression_df = pd.read_csv(
        output_dir / "team_progression_probabilities.csv"
    )
    champion_df = pd.read_csv(
        output_dir / "champion_probabilities.csv"
    )
    calibration_df = pd.read_csv(
        output_dir / "calibration_report.csv"
    )

    assert finalist_df.to_dict("records") == [
        {
            "team": "Alpha",
            "final_probability": 1.0,
        },
        {
            "team": "Beta",
            "final_probability": 1.0,
        },
    ]

    progression = progression_df.set_index("team")
    assert progression.loc["Alpha", "final"] == 1.0
    assert progression.loc["Beta", "final"] == 1.0
    assert progression.loc["Alpha", "champion"] == 1.0
    assert progression.loc["Beta", "champion"] == 0.0

    merged = finalist_df.merge(
        champion_df.rename(
            columns={
                "probability": "championship_probability",
            }
        ),
        on="team",
        how="left",
    ).fillna(
        {
            "championship_probability": 0.0,
        }
    )
    assert (
        merged["final_probability"]
        >= merged["championship_probability"]
    ).all()

    calibration = calibration_df.set_index("metric")
    assert calibration.loc["average_draw_probability", "value"] == 0.1
    assert calibration.loc["high_confidence_matches", "value"] == 1.0
    assert calibration.loc["simulation_runs", "value"] == 1.0


def test_build_match_slot_probabilities_schema_and_values():
    appearances = {
        ("Final", 103, "Alpha"): 3,
        ("Final", 103, "Beta"): 3,
    }
    wins = {
        ("Final", 103, "Alpha"): 2,
        ("Final", 103, "Beta"): 1,
    }

    df = monte_carlo.build_match_slot_probabilities(
        appearances,
        wins,
        simulations=3,
    )

    assert list(df.columns) == [
        "stage",
        "match_id",
        "team",
        "appearances",
        "appearance_probability",
        "wins",
        "slot_win_probability",
        "conditional_win_probability",
        "simulations",
    ]

    alpha = df.set_index("team").loc["Alpha"]
    assert alpha["appearances"] == 3
    assert alpha["appearance_probability"] == 1.0
    assert alpha["wins"] == 2
    assert alpha["slot_win_probability"] == 0.6667
    assert alpha["conditional_win_probability"] == 0.6667


def test_build_most_likely_tournament_path_uses_slot_consensus(
    monkeypatch,
):
    slot_probabilities_df = pd.DataFrame(
        [
            {
                "stage": "Round of 32",
                "match_id": 73,
                "team": "Alpha",
                "slot_win_probability": 0.7,
            },
            {
                "stage": "Round of 32",
                "match_id": 73,
                "team": "Beta",
                "slot_win_probability": 0.3,
            },
            {
                "stage": "Round of 32",
                "match_id": 74,
                "team": "Gamma",
                "slot_win_probability": 0.4,
            },
            {
                "stage": "Round of 32",
                "match_id": 74,
                "team": "Delta",
                "slot_win_probability": 0.6,
            },
            {
                "stage": "Round of 16",
                "match_id": 89,
                "team": "Alpha",
                "slot_win_probability": 0.45,
            },
            {
                "stage": "Round of 16",
                "match_id": 89,
                "team": "Delta",
                "slot_win_probability": 0.55,
            },
        ]
    )
    matchup_appearances = {
        ("Round of 32", 73, "Alpha", "Beta"): 10,
        ("Round of 32", 74, "Gamma", "Delta"): 10,
    }

    monkeypatch.setattr(
        monte_carlo,
        "ROUND_OF_16_STRUCTURE",
        [
            (89, 73, 74),
        ],
    )
    monkeypatch.setattr(
        monte_carlo,
        "QUARTERFINAL_STRUCTURE",
        [],
    )
    monkeypatch.setattr(
        monte_carlo,
        "SEMIFINAL_STRUCTURE",
        [],
    )
    monkeypatch.setattr(
        monte_carlo,
        "FINAL_STRUCTURE",
        [],
    )

    df = monte_carlo.build_most_likely_tournament_path(
        slot_probabilities_df,
        matchup_appearances,
        simulations=10,
    )

    assert list(df.columns) == [
        "stage",
        "match_id",
        "team_1",
        "team_2",
        "winner",
        "loser",
        "winner_slot_probability",
        "team_1_slot_win_probability",
        "team_2_slot_win_probability",
        "simulations",
        "method",
    ]

    final_row = df[df["match_id"] == 89].iloc[0]
    assert final_row["team_1"] == "Alpha"
    assert final_row["team_2"] == "Delta"
    assert final_row["winner"] == "Delta"
    assert final_row["winner_slot_probability"] == 0.55
    assert (
        final_row["method"]
        == "monte_carlo_match_slot_consensus"
    )
