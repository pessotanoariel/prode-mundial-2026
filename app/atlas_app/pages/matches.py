from app.atlas_app.components.matches import render_editorial_hero
from app.atlas_app.components.matches import render_forecast_cards
from app.atlas_app.components.matches import render_match_index
from app.atlas_app.components.matches import render_match_notes
from app.atlas_app.components.matches import render_strongest_forecasts
from app.atlas_app.components.matches import render_surprise_watch


def render(data: dict) -> None:
    predictions_df = data.get("predictions")

    render_editorial_hero(
        predictions_df
    )

    filtered_df, display_limit = render_match_index(
        predictions_df
    )

    render_surprise_watch(
        predictions_df
    )

    render_strongest_forecasts(
        predictions_df
    )

    render_forecast_cards(
        filtered_df,
        display_limit
    )

    render_match_notes(
        filtered_df
    )
