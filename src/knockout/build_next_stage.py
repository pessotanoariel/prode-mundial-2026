from pathlib import Path

import pandas as pd

def extract_previous_match_ids(
    structure
):

    previous_ids = []

    for (
        _,
        previous_1,
        previous_2
    ) in structure:

        previous_ids.extend([
            previous_1,
            previous_2
        ])

    return previous_ids

def build_next_stage(
    winners_path,
    structure,
    output_path
):

    winners_df = pd.read_csv(
        winners_path
    )

    winners = winners_df[
        "winner"
    ].tolist()

    previous_match_ids = (
        extract_previous_match_ids(
            structure
        )
    )

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