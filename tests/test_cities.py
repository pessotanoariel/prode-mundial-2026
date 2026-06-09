import pandas as pd

from app.atlas_app.cities import build_host_city_profiles
from app.atlas_app.cities import host_city_narratives
from app.atlas_app.cities import load_host_city_profiles


def test_host_city_profiles_dataset_schema_and_count():
    profiles_df = load_host_city_profiles()

    assert len(profiles_df) == 16
    assert set(profiles_df.columns) == {
        "host_city",
        "country",
        "stadium",
        "matches",
        "group_matches",
        "knockout_matches",
        "is_final_venue",
        "is_opening_match_venue",
    }


def test_build_host_city_profiles_counts_group_and_knockout_matches():
    match_venues_df = pd.DataFrame([
        {
            "match_number": 1,
            "stage": "Group Stage",
            "host_city": "City A",
            "country": "Country A",
            "stadium": "Stadium A",
        },
        {
            "match_number": 104,
            "stage": "Final",
            "host_city": "City A",
            "country": "Country A",
            "stadium": "Stadium A",
        },
    ])

    profiles_df = build_host_city_profiles(match_venues_df)
    profile = profiles_df.iloc[0]

    assert profile["matches"] == 2
    assert profile["group_matches"] == 1
    assert profile["knockout_matches"] == 1
    assert bool(profile["is_final_venue"]) is True
    assert bool(profile["is_opening_match_venue"]) is True


def test_host_city_narratives_include_final_and_opening_notes():
    profiles_df = load_host_city_profiles()
    notes = host_city_narratives(profiles_df)

    assert any("La final está programada" in note for note in notes)
    assert any("El partido inaugural está programado" in note for note in notes)
    assert any("Estadio Azteca" in note for note in notes)
