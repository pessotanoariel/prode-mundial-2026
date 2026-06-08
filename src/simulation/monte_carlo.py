from collections import Counter
from collections import defaultdict
import logging
from pathlib import Path

import pandas as pd

from src.knockout.tournament import (
    simulation_main
)

from src.knockout.paths import (
    QUARTERFINALS_WINNERS,
    SEMIFINALS_WINNERS,
    FINAL_WINNERS
)


FINAL_WINNERS_PATH = (
    "data/output/final_winners.csv"
)

PREDICTIONS_PATH = Path("data/output/predictions.csv")
CALIBRATION_REPORT_PATH = Path("data/output/calibration_report.csv")
LOG_PATH = Path("execution_logs/latest_run.log")
LOGGER_NAME = "world_cup_forecast_atlas.pipeline"

DEFAULT_SIMULATIONS = 1000

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


def build_calibration_report(
    predictions_path=PREDICTIONS_PATH,
    simulations=DEFAULT_SIMULATIONS
):
    predictions_df = pd.read_csv(
        predictions_path
    )

    confidence_counts = (
        predictions_df["confidence"]
        .str.upper()
        .value_counts()
    )

    rows = [
        {
            "metric": "average_draw_probability",
            "value": round(
                predictions_df["draw_probability"].mean(),
                4
            )
        },
        {
            "metric": "median_draw_probability",
            "value": round(
                predictions_df["draw_probability"].median(),
                4
            )
        },
        {
            "metric": "minimum_draw_probability",
            "value": round(
                predictions_df["draw_probability"].min(),
                4
            )
        },
        {
            "metric": "maximum_draw_probability",
            "value": round(
                predictions_df["draw_probability"].max(),
                4
            )
        },
        {
            "metric": "high_confidence_matches",
            "value": int(confidence_counts.get("HIGH", 0))
        },
        {
            "metric": "medium_confidence_matches",
            "value": int(confidence_counts.get("MEDIUM", 0))
        },
        {
            "metric": "low_confidence_matches",
            "value": int(confidence_counts.get("LOW", 0))
        },
        {
            "metric": "simulation_runs",
            "value": int(simulations)
        },
    ]

    return pd.DataFrame(
        rows,
        columns=[
            "metric",
            "value"
        ]
    )


def get_calibration_logger():
    LOG_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    logger = logging.getLogger(
        LOGGER_NAME
    )

    if not logger.handlers:
        logger.setLevel(
            logging.INFO
        )
        logger.propagate = False

        file_handler = logging.FileHandler(
            LOG_PATH,
            mode="a",
            encoding="utf-8",
        )
        file_handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] %(levelname)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(
            file_handler
        )

    return logger


def write_calibration_report(
    simulations=DEFAULT_SIMULATIONS
):
    report_df = build_calibration_report(
        simulations=simulations
    )

    CALIBRATION_REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )
    report_df.to_csv(
        CALIBRATION_REPORT_PATH,
        index=False
    )

    logger = get_calibration_logger()

    logger.info(
        "CALIBRATION DIAGNOSTICS"
    )

    for _, row in report_df.iterrows():
        logger.info(
            "%s=%s",
            row["metric"],
            row["value"]
        )

    print(
        "\nCalibration Diagnostics\n"
    )

    print(
        report_df
    )

    return report_df


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

    write_calibration_report(
        simulations=simulations
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
