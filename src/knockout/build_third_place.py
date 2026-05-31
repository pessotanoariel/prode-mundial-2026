import pandas as pd

INPUT_PATH = (
    "data/output/semifinals_winners.csv"
)

OUTPUT_PATH = (
    "data/output/third_place.csv"
)


def build_third_place():

    losers_df = pd.read_csv(
        INPUT_PATH
    )

    losers = losers_df[
        "loser"
    ].tolist()

    df = pd.DataFrame([
        {
            "match_id": 104,
            "team_a": losers[0],
            "team_b": losers[1]
        }
    ])

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    return df


if __name__ == "__main__":

    print(
        build_third_place()
    )