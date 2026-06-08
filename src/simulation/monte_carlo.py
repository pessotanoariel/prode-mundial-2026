from collections import Counter

import pandas as pd

from src.knockout.tournament import (
    simulation_main
)

from collections import defaultdict

from src.knockout.paths import (
    QUARTERFINALS_WINNERS,
    SEMIFINALS_WINNERS,
    FINAL_WINNERS
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

    return tuple(
        sorted(
            get_finalists()
        )
    )

def get_finalists():

    df = pd.read_csv(
        FINAL_WINNERS_PATH
    )

    return [
        df.iloc[0]["team_1"],
        df.iloc[0]["team_2"]
    ]


def get_stage_teams(
    winners_path
):

    df = pd.read_csv(
        winners_path
    )

    return df["winner"].tolist()



def run_monte_carlo(
    simulations=DEFAULT_SIMULATIONS
):

    champions = Counter()

    finals = Counter()

    finalists_counter = Counter()

    progression = defaultdict(
        lambda: {
            "qf": 0,
            "sf": 0,
            "final": 0,
            "champion": 0
        }
    )

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

        finalists = get_finalists()

        finals[
            final_matchup
        ] += 1

        champions[
            champion
        ] += 1

        quarterfinalists = (
            get_stage_teams(
                QUARTERFINALS_WINNERS
            )
        )

        semifinalists = (
            get_stage_teams(
                SEMIFINALS_WINNERS
            )
        )

        for team in quarterfinalists:

            progression[
                team
            ]["qf"] += 1


        for team in semifinalists:

            progression[
                team
            ]["sf"] += 1


        for team in finalists:

            finalists_counter[
                team
            ] += 1

            progression[
                team
            ]["final"] += 1


        progression[
            champion
        ]["champion"] += 1

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

    finalist_rows = []

    for team, count in (
        finalists_counter.items()
    ):

        finalist_rows.append({
            "team": team,
            "final_probability": round(
                count / simulations,
                4
            )
        })

    finalist_probabilities_df = (
        pd.DataFrame(
            finalist_rows
        )
        .sort_values(
            "final_probability",
            ascending=False
        )
    )

    finalist_probabilities_df.to_csv(
        "data/output/finalist_probabilities.csv",
        index=False
    )

    print(
        "\nFinalist Probabilities\n"
    )

    print(
        finalist_probabilities_df.head(20)
    )

    progression_rows = []

    for team, stats in (
        progression.items()
    ):

        progression_rows.append({
            "team": team,
            "qf": round(
                stats["qf"] / simulations,
                4
            ),
            "sf": round(
                stats["sf"] / simulations,
                4
            ),
            "final": round(
                stats["final"] / simulations,
                4
            ),
            "champion": round(
                stats["champion"] / simulations,
                4
            )
        })

    progression_df = (
        pd.DataFrame(
            progression_rows
        )
        .sort_values(
            "champion",
            ascending=False
        )
    )

    progression_df.to_csv(
        "data/output/team_progression_probabilities.csv",
        index=False
    )

    print(
        "\nTeam Progression Probabilities\n"
    )

    print(
        progression_df.head(20)
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
