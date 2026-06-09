from collections import Counter
from collections import defaultdict
import logging
from pathlib import Path

import pandas as pd

from src.knockout.tournament import (
    simulation_main
)

from src.knockout.paths import (
    ROUND_OF_32_COMPLETE,
    ROUND_OF_32_WINNERS,
    ROUND_OF_16,
    ROUND_OF_16_WINNERS,
    QUARTERFINALS,
    QUARTERFINALS_WINNERS,
    SEMIFINALS,
    SEMIFINALS_WINNERS,
    FINAL,
    FINAL_WINNERS
)

from src.knockout.structures import (
    ROUND_OF_16_STRUCTURE,
    QUARTERFINAL_STRUCTURE,
    SEMIFINAL_STRUCTURE,
    FINAL_STRUCTURE
)


FINAL_WINNERS_PATH = (
    "data/output/final_winners.csv"
)

PREDICTIONS_PATH = Path("data/output/predictions.csv")
CALIBRATION_REPORT_PATH = Path("data/output/calibration_report.csv")
LOG_PATH = Path("execution_logs/latest_run.log")
LOGGER_NAME = "world_cup_forecast_atlas.pipeline"

DEFAULT_SIMULATIONS = 1000

MATCH_SLOT_PROBABILITIES_PATH = (
    "data/output/knockout_match_slot_probabilities.csv"
)
MOST_LIKELY_TOURNAMENT_PATH = (
    "data/output/most_likely_tournament_path.csv"
)
MOST_LIKELY_PATH_METHOD = (
    "monte_carlo_match_slot_consensus"
)

KNOCKOUT_STAGES = [
    {
        "stage": "Round of 32",
        "matches_path": ROUND_OF_32_COMPLETE,
        "winners_path": ROUND_OF_32_WINNERS,
    },
    {
        "stage": "Round of 16",
        "matches_path": ROUND_OF_16,
        "winners_path": ROUND_OF_16_WINNERS,
    },
    {
        "stage": "Quarterfinals",
        "matches_path": QUARTERFINALS,
        "winners_path": QUARTERFINALS_WINNERS,
    },
    {
        "stage": "Semifinals",
        "matches_path": SEMIFINALS,
        "winners_path": SEMIFINALS_WINNERS,
    },
    {
        "stage": "Final",
        "matches_path": FINAL,
        "winners_path": FINAL_WINNERS,
    },
]

PROGRESSION_STAGE_COLUMNS = {
    "Round of 32": "round_of_32",
    "Round of 16": "round_of_16",
    "Quarterfinals": "quarterfinal",
    "Semifinals": "semifinal",
    "Final": "final",
}

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


def get_team_column(
    row,
    preferred,
    fallback
):

    if preferred in row.index:
        return row[preferred]

    return row[fallback]


def collect_match_slot_results(
    match_slot_appearances,
    match_slot_wins,
    matchup_appearances
):

    for stage_config in KNOCKOUT_STAGES:

        matches_df = pd.read_csv(
            stage_config["matches_path"]
        )
        winners_df = pd.read_csv(
            stage_config["winners_path"]
        )

        for (_, match_row), (_, winner_row) in zip(
            matches_df.iterrows(),
            winners_df.iterrows()
        ):

            stage = stage_config["stage"]
            match_id = int(
                match_row["match_id"]
            )
            team_1 = get_team_column(
                match_row,
                "team_a",
                "team_1"
            )
            team_2 = get_team_column(
                match_row,
                "team_b",
                "team_2"
            )
            winner = winner_row["winner"]

            for team in [
                team_1,
                team_2
            ]:

                match_slot_appearances[
                    (
                        stage,
                        match_id,
                        team
                    )
                ] += 1

            match_slot_wins[
                (
                    stage,
                    match_id,
                    winner
                )
            ] += 1

            matchup_appearances[
                (
                    stage,
                    match_id,
                    team_1,
                    team_2
                )
            ] += 1


def collect_stage_progression_appearances(
    progression
):

    for stage_config in KNOCKOUT_STAGES:

        stage = stage_config["stage"]
        progression_column = (
            PROGRESSION_STAGE_COLUMNS.get(
                stage
            )
        )

        if progression_column is None:
            continue

        matches_df = pd.read_csv(
            stage_config["matches_path"]
        )

        for _, match_row in matches_df.iterrows():

            team_1 = get_team_column(
                match_row,
                "team_a",
                "team_1"
            )
            team_2 = get_team_column(
                match_row,
                "team_b",
                "team_2"
            )

            for team in [
                team_1,
                team_2
            ]:

                progression[
                    team
                ][progression_column] += 1


def build_match_slot_probabilities(
    match_slot_appearances,
    match_slot_wins,
    simulations
):

    rows = []

    slot_keys = sorted(
        match_slot_appearances.keys(),
        key=lambda item: (
            item[1],
            item[2]
        )
    )

    for (
        stage,
        match_id,
        team
    ) in slot_keys:

        appearances = match_slot_appearances[
            (
                stage,
                match_id,
                team
            )
        ]
        wins = match_slot_wins.get(
            (
                stage,
                match_id,
                team
            ),
            0
        )

        rows.append({
            "stage": stage,
            "match_id": match_id,
            "team": team,
            "appearances": appearances,
            "appearance_probability": round(
                appearances / simulations,
                4
            ),
            "wins": wins,
            "slot_win_probability": round(
                wins / simulations,
                4
            ),
            "conditional_win_probability": round(
                wins / appearances,
                4
            ),
            "simulations": simulations
        })

    return pd.DataFrame(
        rows,
        columns=[
            "stage",
            "match_id",
            "team",
            "appearances",
            "appearance_probability",
            "wins",
            "slot_win_probability",
            "conditional_win_probability",
            "simulations"
        ]
    )


def get_slot_win_probability(
    slot_probabilities_df,
    stage,
    match_id,
    team
):

    match = slot_probabilities_df[
        (
            slot_probabilities_df["stage"] == stage
        )
        & (
            slot_probabilities_df["match_id"] == match_id
        )
        & (
            slot_probabilities_df["team"] == team
        )
    ]

    if match.empty:
        return 0.0

    return float(
        match.iloc[0]["slot_win_probability"]
    )


def choose_slot_winner(
    slot_probabilities_df,
    stage,
    match_id,
    team_1,
    team_2
):

    team_1_probability = get_slot_win_probability(
        slot_probabilities_df,
        stage,
        match_id,
        team_1
    )
    team_2_probability = get_slot_win_probability(
        slot_probabilities_df,
        stage,
        match_id,
        team_2
    )

    if team_2_probability > team_1_probability:
        return (
            team_2,
            team_1,
            team_2_probability,
            team_1_probability,
            team_2_probability
        )

    return (
        team_1,
        team_2,
        team_1_probability,
        team_1_probability,
        team_2_probability
    )


def get_most_common_round_of_32_matchups(
    matchup_appearances
):

    matchups = {}

    for (
        stage,
        match_id,
        team_1,
        team_2
    ), count in matchup_appearances.items():

        if stage != "Round of 32":
            continue

        existing = matchups.get(
            match_id
        )

        if (
            existing is None
            or count > existing["count"]
        ):

            matchups[
                match_id
            ] = {
                "team_1": team_1,
                "team_2": team_2,
                "count": count
            }

    return matchups


def append_consensus_match(
    rows,
    winners_by_match_id,
    slot_probabilities_df,
    stage,
    match_id,
    team_1,
    team_2,
    simulations
):

    (
        winner,
        loser,
        winner_probability,
        team_1_probability,
        team_2_probability
    ) = choose_slot_winner(
        slot_probabilities_df,
        stage,
        match_id,
        team_1,
        team_2
    )

    rows.append({
        "stage": stage,
        "match_id": match_id,
        "team_1": team_1,
        "team_2": team_2,
        "winner": winner,
        "loser": loser,
        "winner_slot_probability": round(
            winner_probability,
            4
        ),
        "team_1_slot_win_probability": round(
            team_1_probability,
            4
        ),
        "team_2_slot_win_probability": round(
            team_2_probability,
            4
        ),
        "simulations": simulations,
        "method": MOST_LIKELY_PATH_METHOD
    })

    winners_by_match_id[
        match_id
    ] = winner


def build_most_likely_tournament_path(
    slot_probabilities_df,
    matchup_appearances,
    simulations
):

    rows = []
    winners_by_match_id = {}

    round_of_32_matchups = (
        get_most_common_round_of_32_matchups(
            matchup_appearances
        )
    )

    if not round_of_32_matchups:
        return pd.DataFrame(
            rows,
            columns=[
                "stage",
                "match_id",
                "team_1",
                "team_2",
                "winner",
                "loser",
                "winner_slot_probability",
                "team_1_slot_win_probability",
                "team_2_slot_win_probability",
                "simulations",
                "method"
            ]
        )

    for match_id in sorted(
        round_of_32_matchups
    ):

        matchup = round_of_32_matchups[
            match_id
        ]

        append_consensus_match(
            rows,
            winners_by_match_id,
            slot_probabilities_df,
            "Round of 32",
            match_id,
            matchup["team_1"],
            matchup["team_2"],
            simulations
        )

    stage_structures = [
        (
            "Round of 16",
            ROUND_OF_16_STRUCTURE
        ),
        (
            "Quarterfinals",
            QUARTERFINAL_STRUCTURE
        ),
        (
            "Semifinals",
            SEMIFINAL_STRUCTURE
        ),
        (
            "Final",
            FINAL_STRUCTURE
        ),
    ]

    for stage, structure in stage_structures:

        for (
            match_id,
            previous_1,
            previous_2
        ) in structure:

            append_consensus_match(
                rows,
                winners_by_match_id,
                slot_probabilities_df,
                stage,
                match_id,
                winners_by_match_id[previous_1],
                winners_by_match_id[previous_2],
                simulations
            )

    return pd.DataFrame(
        rows,
        columns=[
            "stage",
            "match_id",
            "team_1",
            "team_2",
            "winner",
            "loser",
            "winner_slot_probability",
            "team_1_slot_win_probability",
            "team_2_slot_win_probability",
            "simulations",
            "method"
        ]
    )


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

    match_slot_appearances = Counter()

    match_slot_wins = Counter()

    matchup_appearances = Counter()

    progression = defaultdict(
        lambda: {
            "round_of_32": 0,
            "round_of_16": 0,
            "quarterfinal": 0,
            "semifinal": 0,
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

        collect_match_slot_results(
            match_slot_appearances,
            match_slot_wins,
            matchup_appearances
        )

        collect_stage_progression_appearances(
            progression
        )

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

        for team in finalists:

            finalists_counter[
                team
            ] += 1

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
            "round_of_32": round(
                stats["round_of_32"] / simulations,
                4
            ),
            "round_of_16": round(
                stats["round_of_16"] / simulations,
                4
            ),
            "quarterfinal": round(
                stats["quarterfinal"] / simulations,
                4
            ),
            "semifinal": round(
                stats["semifinal"] / simulations,
                4
            ),
            "final": round(
                stats["final"] / simulations,
                4
            ),
            "champion": round(
                stats["champion"] / simulations,
                4
            ),
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

    slot_probabilities_df = (
        build_match_slot_probabilities(
            match_slot_appearances,
            match_slot_wins,
            simulations
        )
    )

    slot_probabilities_df.to_csv(
        MATCH_SLOT_PROBABILITIES_PATH,
        index=False
    )

    print(
        "\nKnockout Match Slot Probabilities\n"
    )

    print(
        slot_probabilities_df.head(20)
    )

    most_likely_path_df = (
        build_most_likely_tournament_path(
            slot_probabilities_df,
            matchup_appearances,
            simulations
        )
    )

    most_likely_path_df.to_csv(
        MOST_LIKELY_TOURNAMENT_PATH,
        index=False
    )

    print(
        "\nMost Likely Tournament Path\n"
    )

    print(
        most_likely_path_df
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
