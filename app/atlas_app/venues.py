from functools import lru_cache
from pathlib import Path

import pandas as pd


PROCESSED_DIR = Path("data") / "processed"
STADIUMS_PATH = PROCESSED_DIR / "stadiums.csv"
MATCH_VENUES_PATH = PROCESSED_DIR / "match_venues.csv"
VENUE_TBD = "Venue TBD"

STAGE_MATCH_RANGES = {
    "group": 1,
    "round_of_32": 73,
    "round_of_16": 89,
    "quarterfinals": 97,
    "semifinals": 101,
    "third_place": 103,
    "final": 104,
}


@lru_cache(maxsize=1)
def load_stadiums() -> pd.DataFrame:
    if not STADIUMS_PATH.exists():
        return pd.DataFrame()

    return pd.read_csv(STADIUMS_PATH)


@lru_cache(maxsize=1)
def load_match_venues() -> pd.DataFrame:
    if not MATCH_VENUES_PATH.exists():
        return pd.DataFrame()

    return pd.read_csv(MATCH_VENUES_PATH)


def venue_label(row) -> str:
    stadium = row.get("stadium")
    host_city = row.get("host_city")

    if pd.isna(stadium) or pd.isna(host_city):
        return VENUE_TBD

    return f"{stadium}, {host_city}"


def enrich_matches_with_venues(
    matches_df,
    stage_key: str
) -> pd.DataFrame:
    if matches_df is None or matches_df.empty:
        return pd.DataFrame()

    enriched_df = matches_df.copy()
    start_match_number = STAGE_MATCH_RANGES.get(stage_key)

    if start_match_number is None:
        enriched_df["match_number"] = pd.NA
        enriched_df["stadium"] = VENUE_TBD
        enriched_df["host_city"] = ""
        return enriched_df

    enriched_df["match_number"] = range(
        start_match_number,
        start_match_number + len(enriched_df)
    )

    venues_df = load_match_venues()

    if venues_df.empty:
        enriched_df["stadium"] = VENUE_TBD
        enriched_df["host_city"] = ""
        return enriched_df

    return enriched_df.merge(
        venues_df[
            [
                "match_number",
                "stadium",
                "host_city",
                "venue_code",
            ]
        ],
        on="match_number",
        how="left",
    )
