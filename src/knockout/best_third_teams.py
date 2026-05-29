import pandas as pd


def get_best_third_teams(
    qualified_path="data/output/qualified_teams.csv"
):
    df = pd.read_csv(qualified_path)

    thirds = df[df["position"] == 3].copy()

    thirds = thirds.sort_values(
        by=["PTS", "DG", "GF"],
        ascending=[False, False, False]
    )

    best_thirds = thirds.head(8)

    return best_thirds

if __name__ == "__main__":
    best_thirds = get_best_third_teams()

    print(
        best_thirds[
            ["group", "team", "PTS", "DG", "GF"]
        ]
    )