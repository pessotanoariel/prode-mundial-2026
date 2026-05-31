from pathlib import Path

import pandas as pd


def build_next_stage(
    winners_path,
    structure,
    previous_match_ids,
    output_path
):

    winners_df = pd.read_csv(
        winners_path
    )

    winners = winners_df[
        "winner"
    ].tolist()

    winner_lookup = dict(
        zip(
            previous_match_ids,
            winners
        )
    )

    rows = []

    for (
        match_id,
        previous_1,
        previous_2
    ) in structure:

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

    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path,
        index=False
    )

    return df