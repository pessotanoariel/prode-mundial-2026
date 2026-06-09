from pathlib import Path
from datetime import datetime
import logging

import pandas as pd


TEAMS_TSV_URL = "https://www.eloratings.net/en.teams.tsv"

RAW_OUTPUT_PATH = Path("data/raw/teams_lookup.csv")

LOGGER = logging.getLogger(__name__)

TEAM_COLUMN_NAMES = [
    "country_code",
    "team_name",
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


def _validate_remote_teams(df: pd.DataFrame) -> None:
    if len(df.columns) < len(TEAM_COLUMN_NAMES):
        raise ValueError(
            f"Expected at least {len(TEAM_COLUMN_NAMES)} teams columns, "
            f"received {len(df.columns)}."
        )

    if df.empty:
        raise ValueError("Remote teams source returned no rows.")

    if _contains_html_markers(df):
        raise ValueError("Remote teams source returned HTML.")


def _load_cached_teams_lookup() -> pd.DataFrame:
    if not RAW_OUTPUT_PATH.exists():
        raise FileNotFoundError(
            f"Cached teams lookup file not found: {RAW_OUTPUT_PATH}"
        )

    df = pd.read_csv(RAW_OUTPUT_PATH)
    df.attrs["from_cache"] = True

    return df


def _warn_remote_unavailable() -> None:
    LOGGER.warning("Remote teams source unavailable.")
    print("WARNING - Remote teams source unavailable.")
    print("Using local cached teams_lookup.csv")


def download_teams_lookup() -> pd.DataFrame:

    try:
        df = pd.read_csv(
            TEAMS_TSV_URL,
            sep="\t",
            header=None,
            usecols=[0, 1],
            engine="python"
        )
        _validate_remote_teams(df)
    except Exception:
        _warn_remote_unavailable()
        return _load_cached_teams_lookup()

    df.columns = TEAM_COLUMN_NAMES

    df["extracted_at"] = datetime.now().isoformat(timespec="seconds")
    df["source"] = TEAMS_TSV_URL
    df.attrs["from_cache"] = False

    return df


def main() -> None:

    RAW_OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df = download_teams_lookup()

    if not df.attrs.get("from_cache"):
        df.to_csv(
            RAW_OUTPUT_PATH,
            index=False,
            encoding="utf-8"
        )

        print(f"\nOK - Teams lookup saved to {RAW_OUTPUT_PATH}\n")
    else:
        print(f"\nOK - Teams lookup loaded from {RAW_OUTPUT_PATH}\n")

    print(df.head())


if __name__ == "__main__":
    main()
