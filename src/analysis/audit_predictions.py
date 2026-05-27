from pathlib import Path

import pandas as pd


PREDICTIONS_PATH = Path(
    "data/output/predictions.csv"
)


def audit_predictions() -> None:

    df = pd.read_csv(PREDICTIONS_PATH)

    print("\n==============================")
    print("TOP FAVORITES")
    print("==============================\n")

    favorites = df.sort_values(
        by="team_1_win_probability",
        ascending=False
    )

    print(
        favorites[
            [
                "team_1",
                "team_2",
                "team_1_win_probability",
                "predicted_winner",
                "confidence"
            ]
        ].head(10)
    )

    print("\n==============================")
    print("MOST BALANCED MATCHES")
    print("==============================\n")

    balanced = df.copy()

    balanced["probability_gap"] = (
        abs(
            balanced["team_1_win_probability"]
            - balanced["team_2_win_probability"]
        )
    )

    balanced = balanced.sort_values(
        by="probability_gap",
        ascending=True
    )

    print(
        balanced[
            [
                "team_1",
                "team_2",
                "team_1_win_probability",
                "team_2_win_probability",
                "draw_probability",
                "predicted_winner"
            ]
        ].head(10)
    )

    print("\n==============================")
    print("TOP UPSET RISK MATCHES")
    print("==============================\n")

    upset_matches = df[
        df["upset_risk"].isin(
            ["EXTREME", "HIGH"]
        )
    ]

    print(
        upset_matches[
            [
                "team_1",
                "team_2",
                "predicted_winner",
                "confidence",
                "upset_risk"
            ]
        ]

        .sort_values(
            by="upset_risk"
        )
    )

    print("\n==============================")
    print("CONFIDENCE DISTRIBUTION")
    print("==============================\n")

    print(
        df["confidence"]
        .value_counts()
    )

    print("\n==============================")
    print("POTENTIAL UPSETS")
    print("==============================\n")

    upsets = df[
        (
            df["predicted_winner"]
            != "Draw"
        )
        &
        (
            df["confidence"] == "Low"
        )
    ]

    print(
        upsets[
            [
                "team_1",
                "team_2",
                "predicted_winner",
                "predicted_score"
            ]
        ]
    )


if __name__ == "__main__":
    audit_predictions()