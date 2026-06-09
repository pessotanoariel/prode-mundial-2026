import streamlit as st

from app.atlas_app.components.cover import render_group_dispatch_grid
from app.atlas_app.components.cover import render_magazine_hero
from app.atlas_app.components.cover import render_most_likely_final
from app.atlas_app.components.cover import render_top_favorites
from app.atlas_app.components.cover import render_tournament_teaser


def render(data: dict) -> None:
    champions_df = data.get("champions")
    finals_df = data.get("finals")
    most_likely_path_df = data.get("most_likely_path")
    final_predictions_df = data.get("final")
    standings_df = data.get("standings")
    qualified_df = data.get("qualified")

    render_magazine_hero(
        champions_df,
        finals_df
    )

    favorites_col, final_col = st.columns([1, 1])

    with favorites_col:
        render_top_favorites(champions_df)

    with final_col:
        render_most_likely_final(
            most_likely_path_df
        )

    render_group_dispatch_grid(
        standings_df,
        qualified_df
    )

    render_tournament_teaser(
        final_predictions_df,
        champions_df
    )
