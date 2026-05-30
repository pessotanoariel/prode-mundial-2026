import pandas as pd

INPUT_PATH = (
    "data/output/semifinals_winners.csv"
)

OUTPUT_PATH = (
    "data/output/final.csv"
)


def build_final():

    winners_df = pd.read_csv(
        INPUT_PATH
    )

    winners = winners_df[
        "winner"
    ].tolist()

    df = pd.DataFrame([
        {
            "match_id": 103,
            "team_a": winners[0],
            "team_b": winners[1]
        }
    ])

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(df)


if __name__ == "__main__":
    build_final()