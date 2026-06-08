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
