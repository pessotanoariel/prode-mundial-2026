import pandas as pd

from src.knockout.slot_mapping import build_slot_mapping


def resolve_slot(slot, mapping):
    return mapping.get(slot, slot)


def generate_round_of_32_real_teams(
    structure_path="data/processed/round_of_32_structure.csv",
    output_path="data/processed/round_of_32_real_teams.csv"
):
    structure_df = pd.read_csv(structure_path)

    mapping = build_slot_mapping()

    structure_df["team_a"] = structure_df["team_a_slot"].apply(
        lambda x: resolve_slot(x, mapping)
    )

    structure_df["team_b"] = structure_df["team_b_slot"].apply(
        lambda x: resolve_slot(x, mapping)
    )

    structure_df.to_csv(output_path, index=False)

    print(f"✅ Exported: {output_path}")


if __name__ == "__main__":
    generate_round_of_32_real_teams()