import pandas as pd


def build_slot_mapping(
    qualified_path="data/output/qualified_teams.csv"
):
    df = pd.read_csv(qualified_path)

    slot_mapping = {}

    for _, row in df.iterrows():
        slot = f"{int(row['position'])}{row['group']}"
        slot_mapping[slot] = row["team"]

    return slot_mapping