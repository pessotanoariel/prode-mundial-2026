import pandas as pd


ANNEX_C_PATH = "data/raw/annex_c.xlsx"


def get_annex_c_matchups(best_third_groups):
    """
    best_third_groups:
        ['A','B','C','D','G','H','I','J']

    returns:
        {
            '1A': '3A',
            '1B': '3J',
            ...
        }
    """

    key = "".join(sorted(best_third_groups))

    annex_df = pd.read_excel(ANNEX_C_PATH)

    row = annex_df[
        annex_df["combination"] == key
    ]

    if row.empty:
        raise ValueError(
            f"Combination not found in Annex C: {key}"
        )

    row = row.iloc[0]

    return {
        "1A": row["1A"],
        "1B": row["1B"],
        "1D": row["1D"],
        "1E": row["1E"],
        "1G": row["1G"],
        "1I": row["1I"],
        "1K": row["1K"],
        "1L": row["1L"],
    }

if __name__ == "__main__":

    test_groups = [
        "G",
        "J",
        "D",
        "H",
        "B",
        "A",
        "C",
        "I"
    ]

    print(
        get_annex_c_matchups(test_groups)
    )