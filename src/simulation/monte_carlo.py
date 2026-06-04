from collections import Counter

import pandas as pd

from src.knockout.tournament import (
    main as run_tournament
)


FINAL_WINNERS_PATH = (
    "data/output/final_winners.csv"
)


def get_champion():

    df = pd.read_csv(
        FINAL_WINNERS_PATH
    )

    return df.iloc[0]["winner"]


def run_monte_carlo(
    simulations=10
):

    champions = Counter()

    for simulation in range(
        simulations
    ):

        print(
            f"Simulation {simulation + 1}/{simulations}"
        )

        run_tournament()

        champion = get_champion()

        champions[
            champion
        ] += 1

    return champions


def main():

    champions = run_monte_carlo(
        simulations=10
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