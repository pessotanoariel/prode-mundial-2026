import pandas as pd


INPUT_PATH = (
    "data/output/quarterfinals_winners.csv"
)

OUTPUT_PATH = (
    "data/output/semifinals.csv"
)


SEMIFINAL_STRUCTURE = [
    (101, 97, 98),
    (102, 99, 100)
]


def build_semifinals():

    winners_df = pd.read_csv(
        INPUT_PATH
    )

    winners = winners_df[
        "winner"
    ].tolist()

    winner_lookup = {
        97: winners[0],
        98: winners[1],
        99: winners[2],
        100: winners[3]
    }

    rows = []

    for (
        match_id,
        previous_1,
        previous_2
    ) in SEMIFINAL_STRUCTURE:

        rows.append({
            "match_id": match_id,
            "team_a": winner_lookup[
                previous_1
            ],
            "team_b": winner_lookup[
                previous_2
            ]
        })

    df = pd.DataFrame(rows)

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(df)


if __name__ == "__main__":
    build_semifinals()
