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

def get_final_matchup():

    df = pd.read_csv(
        FINAL_WINNERS_PATH
    )

    return tuple(
        sorted(
            [
                df.iloc[0]["team_1"],
                df.iloc[0]["team_2"]
            ]
        )
    )


def run_monte_carlo(
    simulations=DEFAULT_SIMULATIONS
):

    champions = Counter()

    finals = Counter()

    for simulation in range(
        simulations
    ):

        print(
            f"Simulation {simulation + 1}/{simulations}"
        )

        simulation_main()

        champion = get_champion()

        final_matchup = (
            get_final_matchup()
        )

        finals[
            final_matchup
        ] += 1

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

    final_rows = []

    for matchup, count in (
        finals.items()
    ):

        final_rows.append({
            "team_1": matchup[0],
            "team_2": matchup[1],
            "appearances": count,
            "probability": round(
                count / simulations,
                4
            )
        })

    finals_df = (
        pd.DataFrame(
            final_rows
        )
        .sort_values(
            "appearances",
            ascending=False
        )
    )

    finals_df.to_csv(
        "data/output/most_likely_finals.csv",
        index=False
    )

    print(
        "\nMost Likely Finals\n"
    )

    print(
        finals_df.head(10)
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