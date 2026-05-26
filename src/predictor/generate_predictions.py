from pathlib import Path

import pandas as pd


INPUT_PATH = Path("data/processed/upcoming_matches.csv")

OUTPUT_PATH = Path("data/output/predictions.csv")


def generate_predictions(df: pd.DataFrame) -> pd.DataFrame:

    predictions = []

    for _, row in df.iterrows():

        home_prob = row["team_1_win_expectancy"]
        away_prob = row["team_2_win_probability"]

        if home_prob >= 0.60:
            predicted_winner = row["team_1_name"]
            predicted_score = "2-0"
            confidence = "High"

        elif home_prob >= 0.45:
            predicted_winner = row["team_1_name"]
            predicted_score = "2-1"
            confidence = "Medium"

        elif away_prob >= 0.45:
            predicted_winner = row["team_2_name"]
            predicted_score = "1-2"
            confidence = "Medium"

        else:
            predicted_winner = "Draw"
            predicted_score = "1-1"
            confidence = "Low"

        predictions.append({
            "match_date": row["match_date"],
            "team_1": row["team_1_name"],
            "team_2": row["team_2_name"],
            "team_1_win_probability": round(home_prob, 3),
            "draw_probability": round(row["draw_probability"], 3),
            "team_2_win_probability": round(away_prob, 3),
            "predicted_winner": predicted_winner,
            "predicted_score": predicted_score,
            "confidence": confidence
        })

    return pd.DataFrame(predictions)


def main() -> None:

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    matches_df = pd.read_csv(INPUT_PATH)

    predictions_df = generate_predictions(matches_df)

    predictions_df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8"
    )

    print(f"\nOK - Predictions saved to {OUTPUT_PATH}\n")

    print(predictions_df.head(20))


if __name__ == "__main__":
    main()