from __future__ import annotations

import importlib
import sys
import time
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class PipelineStep:
    name: str
    module: str


@dataclass(frozen=True)
class PipelineSection:
    name: str
    steps: tuple[PipelineStep, ...]


PIPELINE: tuple[PipelineSection, ...] = (
    PipelineSection(
        "INGESTION",
        (
            PipelineStep("Update Elo rankings", "src.ingestion.update_elo"),
            PipelineStep("Update teams lookup", "src.ingestion.update_teams"),
            PipelineStep("Update fixtures", "src.ingestion.update_fixtures"),
            PipelineStep(
                "Update latest results",
                "src.ingestion.update_latest_results",
            ),
        ),
    ),
    PipelineSection(
        "PROCESSING",
        (
            PipelineStep(
                "Build team strength",
                "src.processing.build_team_strength",
            ),
            PipelineStep(
                "Build recent form",
                "src.processing.build_recent_form",
            ),
            PipelineStep(
                "Build upcoming matches",
                "src.processing.build_upcoming_matches",
            ),
        ),
    ),
    PipelineSection(
        "PREDICTIONS",
        (
            PipelineStep(
                "Generate predictions",
                "src.predictor.generate_predictions",
            ),
        ),
    ),
    PipelineSection(
        "GROUP STAGE",
        (
            PipelineStep(
                "Build group standings",
                "src.simulation.build_group_standings",
            ),
        ),
    ),
    PipelineSection(
        "TOURNAMENT",
        (
            PipelineStep("Run knockout tournament", "src.knockout.tournament"),
        ),
    ),
    PipelineSection(
        "MONTE CARLO",
        (
            PipelineStep("Run Monte Carlo simulation", "src.simulation.monte_carlo"),
        ),
    ),
)


EXPECTED_OUTPUTS: tuple[Path, ...] = (
    Path("data/raw/elo_rankings.csv"),
    Path("data/raw/teams_lookup.csv"),
    Path("data/raw/fixtures.csv"),
    Path("data/raw/latest_results.csv"),
    Path("data/processed/team_strength.csv"),
    Path("data/processed/recent_form.csv"),
    Path("data/processed/upcoming_matches.csv"),
    Path("data/output/predictions.csv"),
    Path("data/output/group_standings.csv"),
    Path("data/output/qualified_teams.csv"),
    Path("data/output/round_of_32_complete.csv"),
    Path("data/output/round_of_32_predictions.csv"),
    Path("data/output/round_of_32_winners.csv"),
    Path("data/output/round_of_16.csv"),
    Path("data/output/round_of_16_predictions.csv"),
    Path("data/output/round_of_16_winners.csv"),
    Path("data/output/quarterfinals.csv"),
    Path("data/output/quarterfinals_predictions.csv"),
    Path("data/output/quarterfinals_winners.csv"),
    Path("data/output/semifinals.csv"),
    Path("data/output/semifinals_predictions.csv"),
    Path("data/output/semifinals_winners.csv"),
    Path("data/output/third_place.csv"),
    Path("data/output/third_place_predictions.csv"),
    Path("data/output/third_place_winners.csv"),
    Path("data/output/final.csv"),
    Path("data/output/final_predictions.csv"),
    Path("data/output/final_winners.csv"),
    Path("data/output/champion_probabilities.csv"),
    Path("data/output/most_likely_finals.csv"),
    Path("data/output/team_progression_probabilities.csv"),
)


def print_header(title: str) -> None:
    line = "=" * len(title)
    print(f"\n{line}\n{title}\n{line}")


def get_step_main(module_name: str) -> Callable[[], None]:
    module = importlib.import_module(module_name)

    try:
        return module.main
    except AttributeError as exc:
        raise RuntimeError(f"Module {module_name} does not expose main()") from exc


def run_step(step: PipelineStep) -> None:
    start_time = time.perf_counter()
    print(f"\n-> {step.name}")

    main_func = get_step_main(step.module)
    main_func()

    elapsed = time.perf_counter() - start_time
    print(f"<- Completed {step.name} in {elapsed:.2f}s")


def verify_outputs() -> None:
    missing_outputs = [
        path
        for path in EXPECTED_OUTPUTS
        if not path.exists()
    ]

    if missing_outputs:
        missing = "\n".join(f"- {path}" for path in missing_outputs)
        raise FileNotFoundError(
            "Pipeline completed, but expected outputs are missing:\n"
            f"{missing}"
        )

    print_header("OUTPUT VERIFICATION")
    print(f"OK - {len(EXPECTED_OUTPUTS)} expected CSV outputs found.")


def run_pipeline() -> int:
    total_start_time = time.perf_counter()
    print_header("WORLD CUP FORECAST ATLAS PIPELINE")

    try:
        for section in PIPELINE:
            print_header(section.name)

            for step in section.steps:
                run_step(step)

        verify_outputs()

    except Exception as exc:
        elapsed = time.perf_counter() - total_start_time
        print(f"\nFAILED - {exc}")
        print(f"Total execution time: {elapsed:.2f}s")
        traceback.print_exc()
        return 1

    elapsed = time.perf_counter() - total_start_time
    print(f"\nSUCCESS - Pipeline completed in {elapsed:.2f}s")
    return 0


def main() -> int:
    return run_pipeline()


if __name__ == "__main__":
    sys.exit(main())
