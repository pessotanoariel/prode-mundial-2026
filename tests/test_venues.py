import pandas as pd

from app.atlas_app.venues import enrich_matches_with_venues
from app.atlas_app.venues import load_match_venues
from app.atlas_app.venues import load_stadiums
from app.atlas_app.venues import venue_label


def test_venue_datasets_cover_official_schedule():
    stadiums_df = load_stadiums()
    venues_df = load_match_venues()

    assert len(stadiums_df) == 16
    assert stadiums_df["host_city"].nunique() == 16
    assert len(venues_df) == 104
    assert venues_df["match_number"].min() == 1
    assert venues_df["match_number"].max() == 104


def test_enrich_group_matches_adds_match_venue_columns():
    matches_df = pd.DataFrame([
        {
            "team_1": "Mexico",
            "team_2": "South Africa",
            "predicted_winner": "Mexico",
        }
    ])

    enriched_df = enrich_matches_with_venues(
        matches_df,
        "group"
    )

    assert enriched_df.iloc[0]["match_number"] == 1
    assert enriched_df.iloc[0]["stadium"] == "Estadio Azteca"
    assert enriched_df.iloc[0]["host_city"] == "Ciudad de México"


def test_venue_label_falls_back_when_missing():
    assert venue_label({}) == "Venue TBD"
