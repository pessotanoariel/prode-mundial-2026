from app.atlas_app.components.atlas import render_championship_orbit
from app.atlas_app.components.atlas import render_contenders_and_challengers
from app.atlas_app.components.atlas import render_editorial_hero
from app.atlas_app.components.atlas import render_finals_from_future
from app.atlas_app.components.atlas import render_forecast_notes
from app.atlas_app.components.atlas import render_tournament_narrative


def render(data: dict) -> None:
    champions_df = data.get("champions")
    finals_df = data.get("finals")
    progression_df = data.get("progression")
    final_predictions_df = data.get("final")

    render_editorial_hero(
        champions_df,
        finals_df
    )

    render_championship_orbit(
        champions_df
    )

    render_finals_from_future(
        finals_df
    )

    render_contenders_and_challengers(
        champions_df
    )

    render_tournament_narrative(
        champions_df,
        finals_df,
        progression_df,
        final_predictions_df
    )

    render_forecast_notes()
