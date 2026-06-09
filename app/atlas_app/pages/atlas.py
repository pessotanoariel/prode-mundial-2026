from app.atlas_app.components.atlas import render_championship_orbit
from app.atlas_app.components.atlas import render_editorial_hero
from app.atlas_app.components.atlas import render_finalist_probabilities
from app.atlas_app.components.atlas import render_finals_from_future
from app.atlas_app.components.atlas import render_forecast_notes
from app.atlas_app.components.atlas import render_host_city_profiles
from app.atlas_app.components.atlas import render_tournament_narrative


def render(data: dict) -> None:
    champions_df = data.get("champions")
    finalists_df = data.get("finalists")
    finals_df = data.get("finals")
    progression_df = data.get("progression")
    final_predictions_df = data.get("final")
    host_city_profiles_df = data.get("host_city_profiles")

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

    render_finalist_probabilities(
        finalists_df
    )

    render_tournament_narrative(
        champions_df,
        finals_df,
        progression_df,
        final_predictions_df
    )

    render_host_city_profiles(
        host_city_profiles_df
    )

    render_forecast_notes()
