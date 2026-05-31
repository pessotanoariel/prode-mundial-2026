import pandas as pd


def resolve_knockout_winners(
    predictions_df: pd.DataFrame
) -> pd.DataFrame:

    rows = []

    for _, row in predictions_df.iterrows():

        winner = row["predicted_winner"]
        resolution = "Regular Time"

        if winner == "Draw":

            team_1_prob = row[
                "team_1_win_probability"
            ]

            team_2_prob = row[
                "team_2_win_probability"
            ]

            gap = abs(
                team_1_prob
                - team_2_prob
            )

            if team_1_prob > team_2_prob:
                winner = row["team_1"]
            else:
                winner = row["team_2"]

            if gap >= 0.08:
                resolution = "Extra Time"
            else:
                resolution = "Penalties"

        loser = (
            row["team_2"]
            if winner == row["team_1"]
            else row["team_1"]
        )

        rows.append({
            "team_1": row["team_1"],
            "team_2": row["team_2"],
            "winner": winner,
            "loser": loser,
            "resolution": resolution
        })

    return pd.DataFrame(rows)

def save_winners(
    predictions_path,
    winners_path
):

    predictions_df = pd.read_csv(
        predictions_path
    )

    winners_df = resolve_knockout_winners(
        predictions_df
    )

    winners_df.to_csv(
        winners_path,
        index=False
    )

    return winners_df

def main():

    predictions_df = pd.read_csv(
        "data/output/round_of_16_predictions.csv"
    )

    winners_df = resolve_knockout_winners(
        predictions_df
    )

    print(winners_df)

    winners_df.to_csv(
        "data/output/round_of_16_winners.csv",
        index=False
    )


if __name__ == "__main__":
    main()
