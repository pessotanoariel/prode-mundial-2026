from functools import lru_cache
from pathlib import Path

import pandas as pd


PROCESSED_DIR = Path("data") / "processed"
HOST_CITY_PROFILES_PATH = PROCESSED_DIR / "host_city_profiles.csv"
MATCH_VENUES_PATH = PROCESSED_DIR / "match_venues.csv"
VENUE_TBD = "Venue TBD"


def build_host_city_profiles(match_venues_df: pd.DataFrame) -> pd.DataFrame:
    if match_venues_df is None or match_venues_df.empty:
        return pd.DataFrame(
            columns=[
                "host_city",
                "country",
                "stadium",
                "matches",
                "group_matches",
                "knockout_matches",
                "is_final_venue",
                "is_opening_match_venue",
            ]
        )

    venues_df = match_venues_df.copy()
    venues_df["is_group_match"] = venues_df["stage"].eq("Group Stage")
    venues_df["is_final_match"] = venues_df["stage"].eq("Final")
    venues_df["is_opening_match"] = venues_df["match_number"].eq(1)

    profiles_df = (
        venues_df
        .groupby(
            ["host_city", "country", "stadium"],
            as_index=False
        )
        .agg(
            matches=("match_number", "count"),
            group_matches=("is_group_match", "sum"),
            is_final_venue=("is_final_match", "any"),
            is_opening_match_venue=("is_opening_match", "any"),
        )
    )
    profiles_df["knockout_matches"] = (
        profiles_df["matches"] - profiles_df["group_matches"]
    )

    return profiles_df[
        [
            "host_city",
            "country",
            "stadium",
            "matches",
            "group_matches",
            "knockout_matches",
            "is_final_venue",
            "is_opening_match_venue",
        ]
    ].sort_values(
        ["country", "host_city"]
    ).reset_index(drop=True)


@lru_cache(maxsize=1)
def load_host_city_profiles() -> pd.DataFrame:
    if HOST_CITY_PROFILES_PATH.exists():
        return pd.read_csv(HOST_CITY_PROFILES_PATH)

    if not MATCH_VENUES_PATH.exists():
        return build_host_city_profiles(pd.DataFrame())

    return build_host_city_profiles(
        pd.read_csv(MATCH_VENUES_PATH)
    )


def host_city_narratives(profiles_df: pd.DataFrame) -> list[str]:
    if profiles_df is None or profiles_df.empty:
        return [VENUE_TBD]

    notes = []

    final_venues = profiles_df[
        profiles_df["is_final_venue"].astype(bool)
    ]

    if not final_venues.empty:
        final = final_venues.iloc[0]
        notes.append(
            f"La final está programada en {final['host_city']}."
        )

    opening_venues = profiles_df[
        profiles_df["is_opening_match_venue"].astype(bool)
    ]

    if not opening_venues.empty:
        opening = opening_venues.iloc[0]
        notes.append(
            f"El partido inaugural está programado en {opening['host_city']}, en {opening['stadium']}."
        )

    azteca = profiles_df[
        profiles_df["stadium"].eq("Estadio Azteca")
    ]

    if not azteca.empty:
        mexico_city = azteca.iloc[0]
        notes.append(
            f"{mexico_city['host_city']} concentra el tramo histórico del calendario en el Estadio Azteca."
        )

    busiest = profiles_df.sort_values(
        ["matches", "knockout_matches"],
        ascending=False
    ).iloc[0]
    notes.append(
        f"{busiest['host_city']} aparece como una de las sedes con mayor carga: {int(busiest['matches'])} partidos."
    )

    return notes
