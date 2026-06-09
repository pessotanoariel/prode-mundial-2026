from pathlib import Path

import pandas as pd
import streamlit as st


DATA_ROOT = Path("data")
RAW_DIR = DATA_ROOT / "raw"
OUTPUT_DIR = DATA_ROOT / "output"
PROCESSED_DIR = DATA_ROOT / "processed"

CSV_PATHS = {
    "predictions": OUTPUT_DIR / "predictions.csv",
    "champions": OUTPUT_DIR / "champion_probabilities.csv",
    "finalists": OUTPUT_DIR / "finalist_probabilities.csv",
    "finals": OUTPUT_DIR / "most_likely_finals.csv",
    "most_likely_path": OUTPUT_DIR / "most_likely_tournament_path.csv",
    "progression": OUTPUT_DIR / "team_progression_probabilities.csv",
    "groups": RAW_DIR / "world_cup_groups.csv",
    "standings": OUTPUT_DIR / "group_standings.csv",
    "qualified": OUTPUT_DIR / "qualified_teams.csv",
    "round_of_32": OUTPUT_DIR / "round_of_32_predictions.csv",
    "round_of_16": OUTPUT_DIR / "round_of_16_predictions.csv",
    "quarterfinals": OUTPUT_DIR / "quarterfinals_predictions.csv",
    "semifinals": OUTPUT_DIR / "semifinals_predictions.csv",
    "third_place": OUTPUT_DIR / "third_place_predictions.csv",
    "final": OUTPUT_DIR / "final_predictions.csv",
    "stadiums": PROCESSED_DIR / "stadiums.csv",
    "match_venues": PROCESSED_DIR / "match_venues.csv",
    "host_city_profiles": PROCESSED_DIR / "host_city_profiles.csv",
}


@st.cache_data
def load_csv(path: str) -> pd.DataFrame:
    if not Path(path).exists():
        return pd.DataFrame()

    return pd.read_csv(path)


def load_atlas_data() -> dict[str, pd.DataFrame]:
    data = {}

    for name, path in CSV_PATHS.items():
        data[name] = load_csv(str(path))

    return data
