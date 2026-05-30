import pandas as pd


INPUT_PATH = (
    "data/output/round_of_16_winners.csv"
)

OUTPUT_PATH = (
    "data/output/quarterfinals.csv"
)


QUARTERFINAL_STRUCTURE = [
    (97, 89, 90),
    (98, 91, 92),
    (99, 93, 94),
    (100, 95, 96)
]


def build_quarterfinals():

    winners_df = pd.read_csv(
        INPUT_PATH
    )

    winners = winners_df[
        "winner"
    ].tolist()

    winner_lookup = {
        89: winners[0],
        90: winners[1],
        91: winners[2],
        92: winners[3],
        93: winners[4],
        94: winners[5],
        95: winners[6],
        96: winners[7]
    }

    rows = []

    for (
        match_id,
        previous_1,
        previous_2
    ) in QUARTERFINAL_STRUCTURE:

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
    build_quarterfinals()
