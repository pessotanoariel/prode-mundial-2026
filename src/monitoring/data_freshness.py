from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class FreshnessCheck:
    path: Path
    max_age_days: int


@dataclass(frozen=True)
class FreshnessResult:
    path: Path
    max_age_days: int
    age_days: int | None
    status: str


FRESH = "FRESH"
STALE = "STALE"

FRESHNESS_CHECKS: tuple[FreshnessCheck, ...] = (
    FreshnessCheck(Path("data/raw/elo_rankings.csv"), 7),
    FreshnessCheck(Path("data/raw/fixtures.csv"), 7),
    FreshnessCheck(Path("data/raw/latest_results.csv"), 7),
    FreshnessCheck(Path("data/raw/teams_lookup.csv"), 30),
)


def get_file_age_days(path: Path, now: datetime | None = None) -> int | None:
    if not path.exists():
        return None

    current_time = now or datetime.now()
    modified_time = datetime.fromtimestamp(path.stat().st_mtime)
    age = current_time - modified_time
    return max(age.days, 0)


def validate_data_freshness(
    checks: tuple[FreshnessCheck, ...] = FRESHNESS_CHECKS,
) -> list[FreshnessResult]:
    results: list[FreshnessResult] = []

    for check in checks:
        age_days = get_file_age_days(check.path)
        status = (
            FRESH
            if age_days is not None and age_days <= check.max_age_days
            else STALE
        )
        results.append(
            FreshnessResult(
                path=check.path,
                max_age_days=check.max_age_days,
                age_days=age_days,
                status=status,
            )
        )

    return results


def format_freshness_result(result: FreshnessResult) -> str:
    indicator = "\u2713" if result.status == FRESH else "\u26a0"
    file_name = result.path.name

    if result.age_days is None:
        return f"{indicator} {file_name} (missing)"

    day_label = "day" if result.age_days == 1 else "days"
    return f"{indicator} {file_name} ({result.age_days} {day_label} old)"
