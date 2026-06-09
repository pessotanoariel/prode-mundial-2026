from pathlib import Path
from datetime import datetime
import logging

import pandas as pd


ELO_TSV_URL = "https://www.eloratings.net/World.tsv"

RAW_OUTPUT_PATH = Path("data/raw/elo_rankings.csv")

LOGGER = logging.getLogger(__name__)

ELO_COLUMN_NAMES = [
    "rank",
    "team",
    "country_code",
    "rating",
    "average_rank",
    "average_rating",
    "1_year_rank",
    "1_year_rating",
    "3_year_rank",
    "3_year_rating",
    "rank_change",
    "rating_change",
    "home_rank_change",
    "home_rating_change",
    "away_rank_change",
    "away_rating_change",
    "win_rank_change",
    "win_rating_change",
    "loss_rank_change",
    "loss_rating_change",
    "goal_rank_change",
    "goal_rating_change",
    "matches_total",
    "matches_home",
    "matches_away",
    "matches_neutral",
    "wins",
    "losses",
    "draws",
    "goals_for",
    "goals_against"
]

HTML_MARKERS = (
    "<!doctype",
    "<html",
    "<head",
)


def _contains_html_markers(df: pd.DataFrame) -> bool:
    sample = " ".join(
        df.head(5)
        .astype(str)
        .to_numpy()
        .ravel()
    ).lower()

    return any(marker in sample for marker in HTML_MARKERS)


def _validate_remote_elo(df: pd.DataFrame) -> None:
    if len(df.columns) != len(ELO_COLUMN_NAMES):
        raise ValueError(
            f"Expected {len(ELO_COLUMN_NAMES)} Elo columns, "
            f"received {len(df.columns)}."
        )

    if df.empty:
        raise ValueError("Remote Elo source returned no rows.")

    if _contains_html_markers(df):
        raise ValueError("Remote Elo source returned HTML.")


def _load_cached_elo_rankings() -> pd.DataFrame:
    if not RAW_OUTPUT_PATH.exists():
        raise FileNotFoundError(
            f"Cached Elo rankings file not found: {RAW_OUTPUT_PATH}"
        )

    df = pd.read_csv(RAW_OUTPUT_PATH)
    df.attrs["from_cache"] = True

    return df


def _warn_remote_unavailable() -> None:
    LOGGER.warning("Remote Elo source unavailable.")
    print("WARNING - Remote Elo source unavailable.")
    print("Using local cached elo_rankings.csv")


def download_elo_rankings() -> pd.DataFrame:
    """
    Download world football Elo rankings from TSV source.
    """
    try:
        df = pd.read_csv(
            ELO_TSV_URL,
            sep="\t",
            header=None,
            names=ELO_COLUMN_NAMES
        )
        _validate_remote_elo(df)
    except Exception:
        _warn_remote_unavailable()
        return _load_cached_elo_rankings()

    df["extracted_at"] = datetime.now().isoformat(timespec="seconds")
    df["source"] = ELO_TSV_URL
    df.attrs["from_cache"] = False

    return df


def main() -> None:

    RAW_OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df = download_elo_rankings()

    if not df.attrs.get("from_cache"):
        df.to_csv(
            RAW_OUTPUT_PATH,
            index=False,
            encoding="utf-8"
        )

        print(f"\nOK - Elo rankings saved to {RAW_OUTPUT_PATH}\n")
    else:
        print(f"\nOK - Elo rankings loaded from {RAW_OUTPUT_PATH}\n")

    print(df.head(10))

    print("\nColumns:")
    print(df.columns.tolist())


if __name__ == "__main__":
    main()
