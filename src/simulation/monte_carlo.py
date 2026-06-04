from collections import Counter

import pandas as pd

from src.knockout.tournament import (
    simulation_main
)


FINAL_WINNERS_PATH = (
    "data/output/final_winners.csv"
)

DEFAULT_SIMULATIONS = 100

def get_champion():

    df = pd.read_csv(
        FINAL_WINNERS_PATH
    )

    return df.iloc[0]["winner"]


def run_monte_carlo(
    simulations=DEFAULT_SIMULATIONS
):

    champions = Counter()

    for simulation in range(
        simulations
    ):

        print(
            f"Simulation {simulation + 1}/{simulations}"
        )

        simulation_main()

        champion = get_champion()

        champions[
            champion
        ] += 1

    rows = []

    for team, count in (
        champions.items()
    ):

        rows.append({
            "team": team,
            "championships": count,
            "probability": round(
                count / simulations,
                4
            )
        })

    probabilities_df = (
        pd.DataFrame(rows)
        .sort_values(
            "championships",
            ascending=False
        )
    )

    probabilities_df.to_csv(
        "data/output/champion_probabilities.csv",
        index=False
    )

    print(
    "\nChampion Probabilities\n"
    )

    print(
        probabilities_df
    )

    return champions


def main():

    champions = run_monte_carlo(
        simulations=DEFAULT_SIMULATIONS
    )

    print("\nChampion Counts\n")

    for team, count in (
        champions.items()
    ):

        print(
            f"{team}: {count}"
        )


if __name__ == "__main__":
    main()