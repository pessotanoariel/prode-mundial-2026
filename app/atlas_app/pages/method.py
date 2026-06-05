from app.atlas_app.components.method import render_editorial_notes
from app.atlas_app.components.method import render_forecast_engine
from app.atlas_app.components.method import render_method_hero
from app.atlas_app.components.method import render_monte_carlo
from app.atlas_app.components.method import render_number_meanings
from app.atlas_app.components.method import render_tournament_flow


def render(data: dict) -> None:
    render_method_hero()
    render_forecast_engine()
    render_tournament_flow()
    render_monte_carlo()
    render_number_meanings()
    render_editorial_notes()
